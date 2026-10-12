# Luna-66 — Simon Says Historical Recovery and Contract Prerequisite

**Status:** BLOCKED; historical task definition and source evidence absent.  
**Dispatch chain:** Luna-0 → Luna-66 → Luna-0.  
**Classification:** read-only provenance recovery and bounded design
prerequisite; no benchmark execution.

## Why this prerequisite exists

The authoritative repository at baseline
`f2ce64b1c514d6e2cf5fc9b741418e5c944da59a` contains no Simon Says benchmark
source, task fixture, result, handoff, task contract, dataset split, seed,
readout/training procedure, or metric report. Case-insensitive repository
search and tracked-file search returned no Simon Says material; `git log
--all` and tracked history searches for Simon-specific sources/results also
returned none. The repository's delayed symbolic sequence-memory design
records are distinct work and do not establish that they were the Simon Says
benchmark.

Therefore the original Simon Says task semantics and actual historical
metrics are **not recoverable from the checked repository/references**. No
metric is inferred or supplied. A task title is not enough to decide what a
Simon Says example, correct response, omission, sequence boundary, or
historical score means.

## Required primary evidence before design

The owner must provide at least one identifiable primary source and its
provenance:

- the original benchmark/task contract, or exact source revision/file path
  that defines the task;
- the historical runner and fixtures, if they are not already in that source;
- historical result artifacts/logs sufficient to recover reported metrics,
  split, seeds, and the model/readout/training configuration.

Mark each fact as `REPOSITORY-VERIFIED`, `OWNER-SUPPLIED`, or `NOT RECOVERED`.
Record exact file or Git-object identities. If no primary task definition is
available, stop and ask the owner whether to supply it or explicitly define a
new benchmark; a newly defined task must not be presented as historical
Simon Says.

## Luna-66 scope after evidence is supplied

Luna-66 may only:

1. Reconstruct the original task definition and benchmark protocol without
   modifying its semantics.
2. Recover actual historical metrics, seeds, splits, readout/training
   implementation and known limitations, or explicitly state which records
   remain unavailable.
3. Determine whether each requested analysis below is defined by the
   original task; classify unsupported requests as separate future task
   proposals.
4. Draft a Simon-specific bounded experiment contract, with a distinct
   primary metric and split/control policy, for independent Luna-0 review.
5. Return to Luna-0. Do not start a benchmark experiment.

### Requested probes to map, not to retrofit

The future design must address, only where the recovered task semantics
support them:

- sequence recognition;
- next-event prediction;
- exact sequence reproduction, if the original task expects output replay;
- multiple sequence lengths;
- variable inter-event delays;
- repeated symbols;
- distractor events;
- held-out sequence generalization;
- temporal-order controls.

Separate the primary historical metric from new diagnostics. Original task
inputs, omissions/silence, deadlines, scoring, and class labels may not be
silently changed to accommodate a requested probe.

## Instrumentation and design boundaries

Luna-66 may map requested diagnostics to existing public observables:
source/intermediate/destination events; prediction admissions/matches/errors;
eligibility creation/expiry; reward delivery; queue occupancy; bounded
connectivity/fan-in/fan-out; actual edge use; event-based energy proxy; and
deterministic replay identity. It must identify unsupported fields rather
than create zero-filled claims. Any minimal observer addition requires
separate Luna-0 review and owner authorization before implementation.

Spiral acceptance criteria, seeds, thresholds, split definitions, and results
must not be imported into the Simon Says contract. The tracks remain
independent; there is no combined score or cross-lane model selection.
Luna-64's unused corrective allowance is unavailable and irrelevant.

## Execution status, resource boundary, and next identity

For this governance/recovery stage the Simon Says benchmark budget is exactly
**zero runs, zero generated or scored examples, zero training, zero benchmark
compute, and zero benchmark artifacts**. No Simon Says example, dataset,
training, or benchmark command is authorized or run. A future execution
budget cannot be scientifically specified until the task unit, sequence
lengths, event alphabet, and task duration are recovered. Do not create an
executable command or claim a future budget is ready.

After Luna-66 returns a reviewed source/provenance package and a separate
contract draft, Luna-0 may assign a new, unused Simon Says experiment
identity. That execution identity is intentionally unassigned here; do not
consume an identity or infer authorization from this prerequisite.

## Acceptance and stop conditions

The Luna-66 handoff is complete only if it contains:

- primary source identities and exact baseline revision;
- recovered task semantics, historical metrics, split, seeds, and
  implementation, each with provenance labels;
- explicit unavailable facts and conflict resolutions;
- requested-probe mapping to the original semantics;
- a separate Simon contract proposal with independent acceptance criteria;
- a statement that no workload was run.

If required source evidence remains unavailable, the correct result is
**BLOCKED — SIMON SAYS TASK SEMANTICS UNRECOVERED**. Do not synthesize,
execute, score, or publish replacement historical results.
