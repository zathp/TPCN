# Luna-72A-M2D Baseline and Provenance

## Scope and authorization

The project owner selected M2C successor Option 1: **M2D design and
independent documentary readiness preparation only**. Authorized work includes
static repository/historical inspection, design of an isolated standalone-E1
two-hop harness, interface/provenance/resource/control contracts, independent
Luna-0 documentary review and a future authorization candidate.

Not authorized: executable-source changes, implementation, tests, experiments,
profiling, benchmarking, R3 or production-E2 changes, raising resource limits,
R4, Luna-72B, commit, push, merge or publication. Completion of this packet is
not implementation or execution permission.

## Exact checkout identities

- Luna-72A worktree:
  `C:\Users\Patrick\Documents\ActiveCode\TPCN-luna72a`
- Branch: `experiment/luna72a-competing-path-discovery`
- HEAD: `11b6f52e9aa6725af69bcd3cd098bb2c62e78b76`
- Main checkout:
  `C:\Users\Patrick\Documents\ActiveCode\TPCN`
- Main branch: `governance/luna71b-c4-1-ppc11-freeze`
- Main HEAD: `11b6f52e9aa6725af69bcd3cd098bb2c62e78b76`

Both worktrees were checked at intake. The Luna-72A worktree contains prior
untracked R3/M1/M2/M2C evidence and tests; those historical files remain
unchanged. The main checkout also contains unrelated untracked work. Neither
worktree's untracked files are durable Git history. The M2D packet is being
added only under `experiments/luna72a/results/m2d/`; it is local/untracked and
has the same persistence risk until separately authorized for preservation.
No historical bytes have been reconstructed.

## Historical manifests and evidence verification

| Record | Exact manifest SHA-256 | Verification |
|---|---|---|
| Frozen R3 source | `70e1f44de464ffd4ad16366b76ca7d51f168cccaf199cd97de10276987cff62f` | All 12 manifest-listed files rechecked against the manifest's `files` path-to-SHA-256 map in the current worktree; 12 verified, zero mismatches. M1 and M2 manifests bind this identity. |
| M1 | `04ee13db3d5b8330053411ae4a91f8e9643114ba730272771044e158a884e6ba` | All 33 path/size/hash records rechecked in the current worktree; 33 verified, zero mismatches. |
| M2 | `818465480fc31ba88bdb8c79622f67e00d703d9ff4c4c65cb0df7495af439910` | All nine declared packet files rechecked; nine verified, zero mismatches. |
| M2C | `9c2e5d6c9dae754f1679d86f909e9609ef6a86b2c535d0e00e6b5ccf843d6ec6` | All ten declared packet files rechecked; ten verified, zero mismatches. |

M1/M2/M2C manifest self-hashes above were recomputed over raw file bytes.
Their packet contents remain local and uncommitted.

## Historical dispositions

- **R3:** the execution adjudication records an eight-cell PASS for
  infrastructure/mechanism sanity. It explicitly does not establish recursive
  causal B-X-D relaying. R3 routes from sensory events; its signal-receive
  branch updates/records the destination without onward emission.
- **M1:** bounded profiling passed for its declared prefix; the cause of the
  historical R3 first-cell trace-guard failure is PARTIAL, and complete-cell
  / 192-cell resource feasibility is UNKNOWN. Preserve the distinct
  134,217,728-byte Python traced-current and 536,870,912-byte process current
  RSS limits. Do not substitute traced peak for either current limit.
- **M2:** independent readiness/adjudication BLOCKED before execution; zero M2
  cells and no M2 resource/propagation measurements.
- **M2C:** selected Candidate B as a design recommendation, not an existing
  integrated E1 network path. Independent Luna-0 review was CONDITIONAL for
  owner disposition; its required documentary corrections were resolved.
  M2C did not authorize M2D implementation or execution.

## Architecture authority and known integration gap

ACP-0004 is accepted for staged implementation and defines bounded ordinary
E1 excursions. Its independent E1 closure is recorded in
`workflow/handoffs/luna-0-independent-closure-ACP-0004-E1.md`. At the M2D
baseline, `SingleExcursionNeuron` supplies standalone E1 semantics, whereas
`ExcursionCharacterRuntime` is typed for `MultiExcursionNeuron` (E2). No
integrated E1 network harness is claimed. M2D designs a separate experimental
composition and must not alter E2 or substitute E1 in the frozen R3 runner.

ACP-0008 remains an opt-in experimental slow-integration mechanism and is
excluded from this first M2D design. Prediction, prediction-error, eligibility
and reward modules are also outside the first mechanism probe; their A06/A11
execution checks would be N/A, not PASS. They must not be silently converted
to ordinary excitation.

## Intake actions

The baseline, branch, worktree status, historical manifest digests, and
manifest-bound M1/M2/M2C file hashes were checked read-only. Four separate
read-only analysis lanes were assigned for E1 interfaces, causal provenance,
resource/lifecycle, and counterfactual protocol. No source code, tests,
experiments, profiler or benchmark were run or changed.
