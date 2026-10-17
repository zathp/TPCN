# Luna-72A-M2D Final Adjudication

## Decision

**M2D design-document readiness: PASS.** The isolated ACP-0004 E1 B-X-D
harness proposal, provenance contract, resource/lifecycle limits,
counterfactual protocol, proof obligations, and future implementation
authorization candidate are frozen as a documentary proposal at the stated
baseline. The independent Luna-0 review is recorded in `09`.

**Implementation readiness: NOT GRANTED. Execution/workload readiness: NOT
GRANTED.** This design/readiness task does not authorize implementation,
running tests, experiments, profiling, benchmarking, R4, Luna-72B, commit,
push, merge, or publication. Any successor requires a separate explicit owner
decision and the applicable independent review.

## Frozen baseline and historical evidence

- Worktree: `C:\Users\Patrick\Documents\ActiveCode\TPCN-luna72a`
- Branch: `experiment/luna72a-competing-path-discovery`
- HEAD: `11b6f52e9aa6725af69bcd3cd098bb2c62e78b76`
- Main checkout HEAD at intake: the same revision.
- R3 source manifest SHA-256:
  `70e1f44de464ffd4ad16366b76ca7d51f168cccaf199cd97de10276987cff62f`
- M1 manifest SHA-256:
  `04ee13db3d5b8330053411ae4a91f8e9643114ba730272771044e158a884e6ba`
- M2 manifest SHA-256:
  `818465480fc31ba88bdb8c79622f67e00d703d9ff4c4c65cb0df7495af439910`
- M2C manifest SHA-256:
  `9c2e5d6c9dae754f1679d86f909e9609ef6a86b2c535d0e00e6b5ccf843d6ec6`

All twelve path-to-SHA-256 entries in the frozen R3 source manifest were
rechecked with zero mismatches. The M1, M2, and M2C manifests and their declared
packet files were rehashed as detailed in `01`. These historical results and
their original limits remain unchanged: full-cell/192-cell M1 feasibility is
UNKNOWN; M2 was BLOCKED before execution with zero cells; the R3 infrastructure
pilot is not causal B-X-D evidence.

## Design interpretation and unresolved gates

The proposal is a bounded, fixed, acyclic, three-node/two-edge E1 mechanism
fixture. Its numeric trajectories are analytical design estimates, not
observations. It cannot establish one-to-one relay, task efficacy, resource
qualification, or comparability to the R3 192-cell estimand. R4 remains
**BLOCKED**; Luna-72B remains **DEFERRED**.

The proposal retains the historical Python traced-current limit of
134,217,728 bytes and Windows current-RSS limit of 536,870,912 bytes as
separate constraints. Actual harness feasibility and resource outcomes remain
UNKNOWN pending a separately authorized implementation and qualification.

The exact future file allowlist, proposed interface, fourteen-run protocol,
bounded controls, fail-closed outcomes, observer identity rules, and test
obligations are specified in `08`. The candidate is a request for a separate
owner decision, not an authorization.

## Work performed and persistence boundary

No executable source was edited. No tests, experiments, workloads, profiling,
or benchmarks were run. The independent reviewer performed a read-only
documentary review.

The M2D packet is local and untracked under
`experiments/luna72a/results/m2d/`. The worktree also contains previously
untracked historical R3/M1/M2/M2C evidence, tests, and a source-package
handoff; they were not overwritten or reconstructed. Untracked files are not
durable Git history and remain at risk until separately authorized for
preservation. No commit or publication was performed. A preservation request,
if desired, must be separately scoped to retaining this exact reviewed
documentary packet and must not imply implementation or execution approval.

## Artifact digest note

`11-m2d-artifact-manifest.json` covers the raw bytes of deliverables `01`
through `10`, excluding itself. Its own SHA-256 is recorded separately in the
task completion record to avoid a self-referential manifest entry.
