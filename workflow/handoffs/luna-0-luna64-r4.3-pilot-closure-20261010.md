# Luna-0 — Luna-64 R4.3 bounded pilot closure

```yaml
tpcn_handoff:
  agent: "Luna-0"
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-64 R4.3 pilot independent review and governance closure"
  task_id: "luna64-r4.3-bounded-pilot-closure"
  component: "Independent experiment review and governance"
  status: "closed; pilot not supported as protocol-compliant"
  contract_version: "1.1"
  branch: "governance/luna64-r4.3-freeze-20261010"
  base_revision: "bc338a48bc05f7e15c4cb84636a979294b88e093"
  result_revision: "Governance closure commit containing this record and workflow update."
  dependencies:
    - "Owner authorization record published before experimental dispatch"
    - "Frozen content commit 64a214e310de3b982b90a8ad215598bc1e9f8b1c"
    - "Pilot result commit d709c5aab0a841a8dfb193bd26b306d9b4198392"
    - "Pilot handoff tip d93ef139a1fea46d58cb59a7d7e6325cb1eb8787"
    - "Separate independent Luna-0 review"
  owner: "Repository owner / Luna-0 governance"
  classification: ["INDEPENDENT REVIEW", "PILOT CLOSURE", "NOT ARCHITECTURE ADOPTION"]
  hypothesis: "The reported bounded pilot follows the frozen R4.3 feasibility protocol and its two passes reproduce."
  counter_hypothesis: "Protocol lifecycle violations invalidate the pilot as evidence of faithful R4.3 execution."
  interfaces_relied_on:
    - "R4.3 protocol and golden/schema package"
    - "Published execution source and raw pilot records"
  label_information_boundary:
    - "Review found no label/future-input leakage by record/code inspection."
    - "EVAL records had no target/reward fields; reported EVAL settlement/update counts are zero."
  timing_assumptions:
    - "R4.3 assigns reward delivery, settlement and expiry on the physical event clock."
  reset_boundaries:
    - "The recorded two passes reuse the same input bytes and claim fresh model/episode reset."
  resource_bounds:
    - "Authorized ceiling: 5,184 episodes, 20,736 receptions, 36,716,544 scalar operations, 2,048 operations/event, 256 episode overhead, 900 CPU seconds, 1,200 wall seconds, 512 MiB, 25 MiB artifacts and one logical CPU."
    - "The raw data independently reconciles episodes, receptions and total operations; wall/CPU/affinity/peak-memory telemetry remains supervisor-reported rather than independently observed."
  authorized_scope:
    - "Read-only independent review and artifact reconciliation."
    - "Publish the review disposition and close workflow status."
  unauthorized_scope:
    - "No third workload, repeat run, repaired execution, efficacy study, score calculation, tuning, pooling, production change or architecture promotion."
    - "No Luna-63C modification or reuse."
  controls:
    - "Review performed by a separate Luna-0 agent against the published experimental branch and exact artifacts."
    - "No source/artifact edits or experimental workload execution by reviewer."
    - "Frozen package and 32-entry inventory recomputed against frozen Git objects."
  measurements:
    - "Protocol/code correspondence, raw input/output row counts, replay digests, aggregates, artifact hashes/size, code paths, test results and execution-reported resource readings."
  information_boundary_check:
    - "Artifact and code inspection found no target/future event in EVAL mechanism inputs; dynamic information-flow instrumentation was not performed."
  hardware_mapping:
    - "Software-only experiment; no hardware-equivalence evidence."
  architecture_invariants_touched:
    - "None; no A01-A15 or ACP changes."
  preserves:
    - "Frozen R4.3 package, authorization boundary, production baseline and Luna-63C certificate boundary."
  architecture_change: false
  proposal: null
  files_changed:
    - "This governance closure record."
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
  tests_added: []
  tests_passing:
    - "Frozen R4 validator, R4 tests, focused implementation tests and JavaScript syntax checks."
    - "Independent raw JSONL parsing/digest checks and aggregate reconciliation."
  tests_failed:
    - "Frozen reward timing/lifecycle compliance: runner computed dueTick but applied reward immediately; deadline/expiry lifecycle was absent."
  tests_not_run:
    - "Independent execution of a fresh workload; prohibited after the frozen total workload cap was consumed."
    - "Full repository suite and dynamic information-flow instrumentation."
    - "Efficacy scoring, attribution-specificity replay and all hardware validation."
  assumptions:
    - "The separate review agent's read-only inspection and reported command output are independent evidence; this orchestrator did not execute another scientific workload."
  unresolved:
    - "Faithful R4.3 delayed reward and expiry behavior remains unverified and needs a separately authorized bounded follow-up if pursued."
    - "Scientific efficacy, statistical power, temporal attribution benefit and cost-benefit remain unknown."
  recommended_next_agent:
    - "Project owner to decide whether a new narrowly bounded implementation/mechanism authorization is warranted."
    - "Any additional workload requires a new explicit owner authorization and independent prereview; current pilot budget is exhausted."
```

## Outcome and identity

The owner-authorized R4.3 feasibility-only pilot ran on isolated branch
`experiment/luna64-track-b-r4.3-pilot-20261010`, in
`C:\Users\Patrick\Documents\ActiveCode\TPCN-luna64-r4.3-pilot-20261010`.
The owner authorization was published before dispatch in governance commit
`bc338a48bc05f7e15c4cb84636a979294b88e093`.

- Frozen content commit: `64a214e310de3b982b90a8ad215598bc1e9f8b1c`.
- Governance closure before authorization: `ea1b10456cbf4ca726e473076d239a4f6e53b9c7`.
- R4.3 manifest SHA-256:
  `62D64457BB4BE4FF69F40558D55C6A9FAAA7B9A246DA9F6C6BE4BE8C0348542B`.
- Experimental implementation/result commit:
  `d709c5aab0a841a8dfb193bd26b306d9b4198392`.
- Execution handoff commit / experimental branch tip:
  `d93ef139a1fea46d58cb59a7d7e6325cb1eb8787`.
- Experimental handoff:
  [`luna-64-track-b-r4.3-pilot-20261010.md`](luna-64-track-b-r4.3-pilot-20261010.md).

Independent Luna-0 verdict: **NOT SUPPORTED AS A PROTOCOL-COMPLIANT PILOT**.
This verdict is not a scientific efficacy result. The pilot must not be
treated as evidence for efficacy, attribution specificity, or architecture
value.

## Review evidence

The independent reviewer recomputed the manifest and all ten frozen package
hashes from the freeze objects and reconciled the 32 inventory entries (9
direct raw-byte matches; 23 LF-to-CRLF materializations; 26 unchanged and 6
remapped blob IDs). The experimental diff contains only 11 added paths in
the permitted experimental namespace and the approved handoff path. No
production/core, ACP or Luna-63C path changed.

The reviewer ran the R4 validator and tests, focused pilot tests, and
JavaScript syntax checks. It independently parsed 2,592 input records and
2,592 output records in each pass, reconciled arm/seed aggregates, and
recomputed both identical output digests:

`d71568729476fce3fd346b6d06c37da00dc09e29ea0d076620d4c48ef2ccc39d`

It also recomputed input SHA-256
`0e078601043e6657672fa8db1433d74c73fe8a855eb9242bb85cbb8cea1f061b`.
This is independent artifact reproduction/audit, **not an independent
execution of the workload**.

### Blocking protocol finding

The frozen protocol assigns reward delays and defines reward delivery,
settlement, expiry and cleanup on the physical clock. In the runner,
`run-luna64-r4.3-pilot.mjs` around lines 588–600 computes `dueTick` but calls
`applyRewardOnce(...)` immediately after activation. The helper does not use
the timestamp. Therefore nonzero delays do not delay learning, and the
specified deadline/expiry lifecycle is not exercised. Recorded settlement
counts do not demonstrate delayed settlement. The pilot is not supported as
a faithful R4.3 protocol execution.

## Recorded pilot results and interpretation

The published raw artifacts reconcile to the declared workload:

- six arms, seeds 6401/6402/6403, 96 TRAIN and 48 EVAL episodes per arm/seed;
- 2,592 episodes and 10,368 receptions/pass; 5,184 episodes and 20,736
  receptions in total;
- two pass files are byte-identical, each with SHA-256
  `d71568729476fce3fd346b6d06c37da00dc09e29ea0d076620d4c48ef2ccc39d`;
- raw-derived counted operations: 18,080,352 total, below the authorized
  36,716,544 ceiling; maximum event and episode-operation counters are
  summary-reported as 1,225 and 31, respectively;
- raw/result directory size reported and directory bytes reconciled:
  6,859,499, below 26,214,400 bytes.

The executor reported CPU 1.359 seconds, wall 1.581 seconds, and Windows
process working-set peak 39,280,640 bytes under the respective ceilings;
its runner reported CPU 1.312 seconds, wall 1.424752 seconds, and
74,706,944 bytes. The executor also reports pre-run affinity mask `0x1`.
The reviewer did not independently observe that process or its supervisor
telemetry. Both reported memory values are under the cap. Treat these as
execution-reported measurements, not independently reproduced measurements.

The arm coverage and resource-cost operation totals are auditable from raw
records, but this pilot did not score any arm for efficacy or attribution.
Per-arm operation counts across both passes were: A_COST_ONLY 3,456;
U_UNIFORM_PC 3,697,632; R_RECENCY_PC 3,701,088; L_LINEAR_TEMPORAL
3,282,912; N_NONLINEAR_LOCAL 3,697,632; X_TEMPORAL_DISRUPTION 3,697,632.
These are counted software operations, not physical energy. No per-arm
classification, attribution-specificity, temporal-credit benefit, or
cost-per-correct comparison was produced.

| Review area | Disposition |
|---|---|
| Frozen identity, branch ancestry, path isolation, Luna-63C boundary | PASS |
| R4 validator, focused tests, syntax checks | PASS |
| Workload shape, arm/seed/pass coverage, input records | PASS |
| Deterministic digest match and raw artifact reconciliation | PASS for retained artifacts |
| Event identity and X temporal mapping | PASS |
| Label/future-input isolation | PASS by record/code inspection; no dynamic taint check |
| Reward idempotency helper | PASS in focused unit test |
| Assigned delayed-reward delivery and expiry/deadline lifecycle | FAIL |
| Mathematical/state equations | PARTIAL; static inspection consistent, runner transition not golden-tested end-to-end |
| Hard counter maxima, CPU/wall/affinity/peak memory telemetry | PARTIAL; executor-reported, not independently observed |
| Independent experimental workload execution | NOT RUN |
| Efficacy, statistical reproducibility, attribution, cost-benefit | NOT ASSESSED |
| Full repository tests, dynamic information-flow checks, hardware | NOT RUN |

## Resource closure and next gate

The authorized workload and episode/reception budgets are consumed. Do not
rerun, repair-and-rerun, append a third pass, run counterfactual omission
replay, or start an efficacy run under the current authorization. A new
owner authorization is required before any additional workload. If the
owner elects to continue, the next bounded prerequisite should separately
test delayed delivery and the deadline/expiry/reset lifecycle against the
frozen rules before an independently reviewed proposal requests new
experimental capacity. Do not alter the frozen R4.3 package or score/pool
this pilot as efficacy evidence.

No production integration, architecture promotion, ACP adoption, or
Luna-63C dependency follows from this closure.
