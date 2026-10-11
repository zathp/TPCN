# Luna-0 — Owner authorization: Luna-64 R4.3 bounded pilot

```yaml
tpcn_handoff:
  agent: "Luna-0"
  luna_identifier: "Luna-0"
  descriptive_name: "Luna-64 R4.3 bounded pilot authorization"
  task_id: "luna64-r4.3-bounded-pilot-authorization"
  component: "Governance authorization"
  status: "authorized; execution pending publication and isolated dispatch"
  contract_version: "1.1"
  branch: "governance/luna64-r4.3-freeze-20261010"
  base_revision: "ea1b10456cbf4ca726e473076d239a4f6e53b9c7"
  result_revision: "Containing authorization-record commit; recorded externally by its Git commit identity."
  dependencies:
    - "Frozen R4.3 content commit 64a214e310de3b982b90a8ad215598bc1e9f8b1c"
    - "Governance closure commit ea1b10456cbf4ca726e473076d239a4f6e53b9c7"
    - "R4.3 manifest SHA-256 62D64457BB4BE4FF69F40558D55C6A9FAAA7B9A246DA9F6C6BE4BE8C0348542B"
    - "Independent post-publication freeze review: PASS — IMMUTABLE FREEZE VERIFIED"
  owner: "Repository owner; explicit authorization recorded in the 2026-10-10 task conversation"
  classification: ["GOVERNANCE", "BOUNDED EXPERIMENT AUTHORIZATION", "NOT ARCHITECTURE ADOPTION"]
  hypothesis: "The frozen, deterministic pilot can execute within its declared software-resource limits and reproduce the same canonical output digests on its two matched workload passes."
  counter_hypothesis: "The pilot exceeds a hard cap, violates a scientific/protocol boundary, or fails exact deterministic replay."
  interfaces_relied_on:
    - "Frozen Luna-64 R4.3 protocol, schema, golden fixtures, validator and manifest"
    - "Bounded local event, eligibility, reward and output-digest rules in R4.3"
  label_information_boundary:
    - "Labels, correctness and evaluator-only counterfactuals remain outside decoder inputs."
    - "No evaluation rewards, settlements or learner updates."
  timing_assumptions:
    - "Use R4.3 physical timestamps, event identity ordering, decoder-time policy and reward-delay assignment without revision."
  reset_boundaries:
    - "Reset all model parameters and episodic state before pass two; reuse the exact input bytes and per-episode seeds."
  resource_bounds:
    - "One logical CPU core; 900 CPU seconds; 1,200 wall seconds."
    - "512 MiB process working set."
    - "At most 5,184 workload episodes and 20,736 input receptions total over exactly two passes."
    - "At most 36,716,544 counted scalar operations total, enforced by the R4.3 per-decoder-event and per-episode ceilings."
    - "At most 25 MiB total artifacts; no network, GPU or hardware dependency."
  authorized_scope:
    - "Create the isolated experimental worktree and branch only after this record is committed and published."
    - "Implement the frozen R4.3 experimental specification in the permitted experimental namespace."
    - "Run required correctness/protocol validation and the exact two-pass feasibility pilot."
    - "Retain raw measurements, summaries, configuration, revision, seed and artifact provenance."
    - "Commit and publish the experimental implementation and pilot artifacts for independent review."
  unauthorized_scope:
    - "Any change to the ten frozen R4.3 package files, the 32-entry governing-input inventory, the freeze commits or their recorded identities."
    - "Counterfactual per-event omission replay, efficacy estimation, extra arms/seeds/episodes/passes, seed replacement, pilot pooling, or behavior-based tuning."
    - "Full-scale training/evaluation, benchmark expansion, architecture promotion, ACP adoption, production/default integration or hardware-equivalence claims."
    - "Any Luna-63C modification, reuse, dependency, reinterpretation, or claim that Track B resolves Luna-63C issues."
    - "Any change outside `experiments/luna64/` for implementation/tests/artifacts and the specifically approved Luna-64 governance handoffs under `workflow/handoffs/`."
  controls:
    - "The ten package identities and all 32 inventory identities were checked against the frozen commit before authorization."
    - "Frozen protocol, schema, golden fixtures, manifest, inventory and provenance attestation are read-only."
    - "Any resource, path, schema, replay, protocol or scientific boundary breach stops execution immediately; do not increase caps or replace work."
    - "Independent Luna-0 review must reproduce the experiment from the published artifacts before a scientific verdict."
  measurements:
    - "Exact per-arm/per-seed raw pilot outcomes and canonical output digests for both passes."
    - "CPU/wall time, working-set peak, episodes, receptions, counted operations and artifact bytes."
    - "Per-arm comparison summaries and temporal-attribution measurements only where defined and allowed by R4.3; no efficacy claim from the pilot."
  information_boundary_check:
    - "Verify no label/future-event/evaluator statistic enters mechanism inputs; EVAL has no reward settlement."
  hardware_mapping:
    - "Software-only feasibility pilot; no hardware-equivalence claim."
  architecture_invariants_touched:
    - "None; A01-A15 remain unchanged."
  preserves:
    - "The R4.3 freeze and all ten package identities."
    - "The 32-entry governing-input inventory and Luna-63C certificate boundary."
    - "Existing production behavior and architecture contract."
  architecture_change: false
  proposal: null
  files_changed:
    - "This authorization record."
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
  tests_added: []
  tests_passing:
    - "Pre-authorization package and inventory identity verification against the frozen commit."
    - "Published remote branch resolves to governance closure commit ea1b10456cbf4ca726e473076d239a4f6e53b9c7."
  tests_failed: []
  tests_not_run:
    - "Pilot implementation, protocol tests and experiment are pending published authorization and isolated Luna-64 dispatch."
  assumptions:
    - "The conversation request is the repository owner's explicit approval for this exact R4.3 bounded pilot."
  unresolved:
    - "Pilot feasibility and scientific efficacy are unknown; the bounded pilot cannot establish efficacy."
    - "A new authorization and independent protocol review are required for any full-scale efficacy execution or scope expansion."
  recommended_next_agent:
    - "Luna-64 to implement and execute only the approved bounded pilot in the isolated worktree."
    - "A separate independent Luna-0 reviewer to reproduce and assess the published result."
```

## Owner approval and frozen identity

The repository owner explicitly authorized the **frozen R4.3 bounded
feasibility-only pilot** in the task conversation on 2026-10-10. This records
that approval; it does not infer approval for any other run or change.

- Content freeze: `64a214e310de3b982b90a8ad215598bc1e9f8b1c`.
- Governance closure: `ea1b10456cbf4ca726e473076d239a4f6e53b9c7`.
- Manifest SHA-256: `62D64457BB4BE4FF69F40558D55C6A9FAAA7B9A246DA9F6C6BE4BE8C0348542B`.
- Frozen package: exactly 10 manifest-listed files.
- Governing-input inventory: exactly 32 entries.
- Published Stage-B attestation: `3c65f572482211f0c771596fc9852f7e4a1ce994`.
- Independent remote post-publication review: **PASS — IMMUTABLE FREEZE VERIFIED**.

The exact package and inventory identities were independently recomputed from
the content-freeze Git objects immediately before this authorization was
written. The ten package hashes, published blob IDs, 32 inventory raw hashes,
recorded Git identities/remappings, remote ref, ancestry and applicable
path-scoped attributes were checked. The R4.3 proposal, protocol, schema,
goldens, inventory, manifest and attestation remain unchanged.

## Approved pilot and resource ceilings

The only approved scientific execution is the frozen R4.3 feasibility-only
pilot: six arms × seeds `{6401, 6402, 6403}` × 144 workload episodes per arm
and seed, or **2,592 episodes per pass**. Run exactly two passes, resetting
parameters and episodic state before pass two, with identical input bytes
and per-episode seeds. Compare canonical output digests. A mismatch aborts
the pilot. Retain partial results from any aborted pass; do not replace seeds,
episodes or passes.

Hard ceilings across the two passes:

- one logical CPU core; **900 CPU seconds** and **1,200 wall seconds**;
- **512 MiB** process working set;
- **5,184 episodes**, **20,736 input receptions**;
- **36,716,544 counted scalar operations**, including the R4.3 limits of
  2,048 per decoder event and 256 episode-level operations;
- **25 MiB** total artifacts; no network, GPU or hardware dependency.

Stop immediately on a ceiling breach or any schema, path, protocol,
deterministic-replay or scientific-boundary violation. Do not raise a cap,
retry an aborted workload, substitute a protocol, or tune based on observed
pilot behavior. EVAL receives no correctness reward, reward settlement or
learner update. Counterfactual omission replay is excluded (zero pilot
passes); the pilot is not scored for efficacy and cannot be pooled into a
later efficacy result.

## Permitted paths and protections

Implementation, focused tests and pilot artifacts may be added only under
`experiments/luna64/`, without editing any frozen R4.3 package or inventory
file. Luna-64 execution and result handoffs may be added only as approved
files under `workflow/handoffs/`. The authorization itself and workflow
status are governed on the governance branch.

No production/core, architecture contract, ACP, generic workflow,
Luna-63C contract, fixture, certificate, evidence, authorization or
corrective-reconciliation file may be modified. Luna-63C is an isolation
boundary, not an input, control, source of implementation, or target of this
experiment. No production integration, architecture promotion, or
hardware-equivalence claim follows from this authorization.

## Independent review and next gate

Luna-64 must publish the exact experimental revision, configuration, seeds,
raw measurements, outcomes and artifact hashes. A separate independent
Luna-0 reviewer must reproduce the pilot from those published artifacts and
assess protocol compliance, mathematical correctness, event identity and
temporal selectivity, reward provenance/idempotency, bounded state,
negative controls, deterministic reproducibility, cost-benefit accounting,
resource compliance, artifact hashes and Luna-63C isolation. Passing tests
alone are not scientific efficacy.

This authorization does **not** authorize full-scale Track B execution,
efficacy claims, production integration, ACP adoption or architecture
promotion. Any such work requires a new bounded proposal, independent review
and explicit owner authorization.
