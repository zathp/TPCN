# Luna-64 R4.3 bounded feasibility-only pilot — execution handoff

## Dispatch and disposition

```yaml
tpcn_handoff:
  agent: "Luna-64"
  luna_identifier: "Luna-64"
  task_id: "track-b-local-temporal-reward-decoder"
  gate_id: "L64-TB-GATE-20261010-R4"
  protocol_revision: "4.3.0-draft"
  status: "bounded feasibility pilot completed; independent review pending"
  pilot_type: "feasibility-only"
  scientific_efficacy_verdict: "NOT ASSESSED"
  architecture_promotion: false
  branch: "experiment/luna64-track-b-r4.3-pilot-20261010"
  worktree: "C:\\Users\\Patrick\\Documents\\ActiveCode\\TPCN-luna64-r4.3-pilot-20261010"
  authorized_baseline: "bc338a48bc05f7e15c4cb84636a979294b88e093"
  execution_revision: "bc338a48bc05f7e15c4cb84636a979294b88e093"
  result_commit: "d709c5aab0a841a8dfb193bd26b306d9b4198392"
  result_commit_push: "PASS; origin/experiment/luna64-track-b-r4.3-pilot-20261010 resolves to result_commit"
  review: "Independent Luna-0 reproduction and review still required"
  scope_exit: "No production/core changes, ACP, architecture adoption, Luna-63C changes, or hardware claims"
```

This report records the completed, authorized R4.3 feasibility pilot only.
It does not claim efficacy, cost-benefit success, causal identification, or
architecture adoption. The experimental result commit was pushed to the
specified branch; the handoff itself is a separate documentation-only
addition to the same branch.

## Freeze, authorization, and boundaries

- Execution used the isolated worktree and branch named above. At launch,
  `HEAD` was the owner-authorized baseline `bc338a48bc05f7e15c4cb84636a979294b88e093`.
- The frozen Stage-A content object was
  `64a214e310de3b982b90a8ad215598bc1e9f8b1c`; the reviewed manifest SHA-256
  is `62D64457BB4BE4FF69F40558D55C6A9FAAA7B9A246DA9F6C6BE4BE8C0348542B`.
- The separate owner authorization was present and published before
  execution. The frozen protocol's historical candidate-status fields were
  not edited or treated as the authorization record.
- Identity checks were made before and after the pilot against freeze Git
  objects and the published Stage-B attestation, not by comparing all
  historical inventory checkout bytes with the later governance checkout.
  The exact ten package raw hashes and published object IDs matched. All 32
  inventory identities matched: nine direct raw-blob matches and 23 exact
  LF-to-CRLF materializations, using the attested package OID remappings.
  No identity failure occurred. This includes the intentionally later
  owner-authorization workflow update present at the authorized baseline.
- Only new files below `experiments/luna64/` and this exact approved execution
  handoff were added. No frozen package, inventoried input, protocol,
  schema, golden, validator, generator, attestation, authorization,
  workflow-status, production/core, or Luna-63C file was changed.
- The new `experiments/luna64/.gitattributes` pins LF bytes only for the two
  new pilot scripts and files below `pilot-20261010/`. Checks confirmed it
  does not override the attributes or checkout bytes of the frozen R4.3
  protocol or the authorization handoff.

## Exact bounded workload

- Six frozen arms in protocol order:
  `A_COST_ONLY`, `U_UNIFORM_PC`, `R_RECENCY_PC`, `L_LINEAR_TEMPORAL`,
  `N_NONLINEAR_LOCAL`, `X_TEMPORAL_DISRUPTION`.
- Fixed seeds: `6401`, `6402`, `6403`.
- Each arm/seed: 96 TRAIN and 48 EVAL workload episodes.
- Exactly two passes: 2,592 episodes/pass; 5,184 total episodes.
- Four input receptions/episode: 10,368/pass; 20,736 total.
- 4,320 PCN episodes and 17,280 PCN input receptions total.
- One immediate `activity-cost-proxy` charge per received input, exactly
  once; reward charge zero. Total event charges: 20,736.
- TRAIN delays came from the frozen ordered schedule
  `[0, 1000000, 8000000, 9000000, 15000000, 16000000]` using
  `split_local_ordinal mod 6`, shared across matched arms and seeds.
  TRAIN-only evaluator correctness was applied after prediction/capture.
  The signed reward was settled once under a stable per-episode identity.
- EVAL workload bytes contain no target or reward-delay field. EVAL performed
  no correctness reward, settlement, or parameter update; trained parameter
  hashes were checked before and after the frozen evaluation workload.
- Counterfactual omission replay: zero passes. No efficacy, accuracy,
  attribution-specificity, success/failure, or cost-benefit score was
  calculated. Pilot outcomes were not pooled or designated for future
  efficacy data.
- The exact generated input bytes were saved once and reused in pass two;
  SHA-256 for that byte stream is
  `0e078601043e6657672fa8db1433d74c73fe8a855eb9242bb85cbb8cea1f061b`.
  All model parameters and episodic state were freshly initialized before
  pass two.

## Replay and results

The raw pass files contain all 2,592 canonical episode records in protocol
order for each pass. Their JSONL bytes are identical. SHA-256 over each
canonical compact-JSONL stream, including the required LF after every
episode record:

```text
pass 1  d71568729476fce3fd346b6d06c37da00dc09e29ea0d076620d4c48ef2ccc39d
pass 2  d71568729476fce3fd346b6d06c37da00dc09e29ea0d076620d4c48ef2ccc39d
```

Recomputed digests match the declarations in `run-summary.json`; the
per-pass raw-record field order, record count, four-event shape, prediction
domain, and trained-parameter hash shape were rechecked. All 18 arm/seed
groups are present in each pass summary. Evaluation parameter hashes remain
constant within each seed/arm evaluation sequence.

| Bounded measure | Observed | Hard limit |
|---|---:|---:|
| Episodes | 5,184 | 5,184 |
| Input receptions | 20,736 | 20,736 |
| Counted scalar operations | 18,080,352 | 36,716,544 |
| Maximum operations in one decoder event | 1,225 | 2,048 |
| Maximum episode-level operations | 31 | 256 |
| TRAIN reward records created / settled | 3,456 / 3,456 | one per TRAIN episode |
| Duplicate reward deliveries | 0 | no duplicate update |
| EVAL reward records / updates | 0 / 0 | 0 / 0 |
| Data/result artifact directory | 6,859,499 bytes | 26,214,400 bytes |

Required additional counters, reported in `run-summary.json`: 552,960 tanh
calls; 38,880 exp calls; 6,445,440 parameter reads; 475,200 parameter
writes; 2,920,320 state reads; 86,400 state writes; maximum logical
eligibility storage 766 bytes; maximum logical model/state storage 400
bytes. The model/state figure is 45 binary64 parameters (360 bytes), four
binary64 latent values (32 bytes), and one 64-bit decoder timestamp (8
bytes). The eligibility estimate uses 144 fixed bytes plus the UTF-8 event
ID for each retained event, and the captured five-binary64 credit vector
plus reward ID. These are bounded logical payload counts, not JavaScript
object/allocator overhead; process working set is measured separately. The
operation proxy counts executed scalar addition, subtraction,
multiplication, division, and comparison in decoder, eligibility, reward,
and lifecycle arithmetic. It excludes indexing/loop work, memory accesses,
serialization, hashing, tanh, and exp, which are reported separately or
excluded by protocol. These are software counters, not joules or hardware
energy.

### Resource enforcement and measurement

Windows one-core enforcement was tested rather than assumed. The pilot
process was started behind an input gate, assigned with
`SetProcessAffinityMask`, and queried with `GetProcessAffinityMask`; the
verified child process mask was exactly `0x1` before the workload received
its GO signal. A PowerShell supervisor polled the process every 50 ms for
CPU time, wall time, and Windows peak working set; the runner independently
checked its limits and artifact size after each episode.

| Measure | Pilot runner | Windows supervisor | Limit |
|---|---:|---:|---:|
| CPU time | 1.312 s | 1.359 s | 900 s |
| Wall time | 1.424752 s | 1.581 s | 1,200 s |
| Peak resident/working-set sample | 74,706,944 bytes | 39,280,640 bytes | 536,870,912 bytes |

The two memory APIs reported different peaks; both are retained above and
both are below the cap. The larger runner-observed value is the conservative
comparison. No network, GPU, hardware, or hardware-equivalence dependency
was used.

After execution, the summary was enriched with the separately captured
Windows supervisor measurements and its aggregate artifact-byte total was
reconciled to the exact directory size. No input or raw pass JSONL bytes
were changed, and no workload was rerun or replaced. Final artifacts remain
below the 25 MiB limit.

## Tests and commands

Required frozen protocol/correctness tests passed before implementation
work proceeded, and were rerun after the pilot:

```text
node experiments/luna64/test-track-b-gate-r4.mjs
PASS: PCN transitions 3; generator fixtures 2; bootstrap fixtures 2;
      verdict fixtures 19; CLI validator negatives 20; public valid/invalid CLI
```

Implementation and focused bounded-mechanics checks passed before execution
and again before commit:

```text
node --check experiments/luna64/run-luna64-r4.3-pilot.mjs
node --check experiments/luna64/test-luna64-r4.3-pilot.mjs
node experiments/luna64/test-luna64-r4.3-pilot.mjs
PASS: generator fixtures, 2,592 workload-input records, temporal disruption,
      no EVAL truth fields, one-charge identity, reward idempotency, operation
      caps, initial parameter reset identity
```

The pilot was invoked through the Windows affinity-gated supervisor, which
set and verified the process mask before releasing the runner. Post-run
checks independently recomputed both canonical JSONL hashes and the input
workload hash, validated the exact pass counts and output record shape,
checked all caps and EVAL constraints, and verified the package/inventory
identities at the freeze objects. `git diff --cached --check` passed.

An initial development run of the new mechanics test exposed an incorrect
test assertion about which arm's disrupted decoder timestamp to compare;
the assertion was corrected and all required tests passed before the pilot
was started. This was not a pilot run or a change to R4.3.

The full repository test suite was not run; no production/core files changed.

## Configuration and artifact provenance

Full frozen configuration and seed/input provenance:
`experiments/luna64/pilot-20261010/configuration.json`.
Per-episode raw outcomes and canonical inputs:
`pass-1-episodes.jsonl`, `pass-2-episodes.jsonl`, and
`input-workload.jsonl`. Per-arm/seed/pass accounting:
`pass-1-summary.json`, `pass-2-summary.json`, and `run-summary.json`.
Implementation and focused tests:
`run-luna64-r4.3-pilot.mjs`, `test-luna64-r4.3-pilot.mjs`.

SHA-256 identities at result commit `d709c5aab0a841a8dfb193bd26b306d9b4198392`:

| File | SHA-256 |
|---|---|
| `experiments/luna64/.gitattributes` | `fc05b1f3f28595de657c25294e873f3d17757206891ea01dcbc47d080b0e319f` |
| `experiments/luna64/run-luna64-r4.3-pilot.mjs` | `386fd0db9676f81e16a5ba6b106635018eaf874c5c116fa7fabe15aecfa07422` |
| `experiments/luna64/test-luna64-r4.3-pilot.mjs` | `6c5c958ca1e9266e657f156680f8b487c72fc33c68ae6505a5d9e768a7453ab9` |
| `experiments/luna64/pilot-20261010/configuration.json` | `1c2998350b842661e0c75225fa02dffe6ca8f055bcd394160ce622ea248a6c35` |
| `experiments/luna64/pilot-20261010/input-workload.jsonl` | `0e078601043e6657672fa8db1433d74c73fe8a855eb9242bb85cbb8cea1f061b` |
| `experiments/luna64/pilot-20261010/pass-1-episodes.jsonl` | `d71568729476fce3fd346b6d06c37da00dc09e29ea0d076620d4c48ef2ccc39d` |
| `experiments/luna64/pilot-20261010/pass-1-summary.json` | `4f33d193b879d24b3e5688d19ef094ba6ea15bb6589a3cd2d332451e54fbaa48` |
| `experiments/luna64/pilot-20261010/pass-2-episodes.jsonl` | `d71568729476fce3fd346b6d06c37da00dc09e29ea0d076620d4c48ef2ccc39d` |
| `experiments/luna64/pilot-20261010/pass-2-summary.json` | `1ccb4e889c73126cef3f4562398afc49a6c35f4775e6d92463bea044260bc623` |
| `experiments/luna64/pilot-20261010/run-summary.json` | `6ab44664c8e5cb0739dd533665b93c66fdeb5be4159fad660c04a76a785102c2` |

## Commit, publication, and next gate

- Result/artifact commit:
  `d709c5aab0a841a8dfb193bd26b306d9b4198392`.
- Push result: successful; the remote
  `refs/heads/experiment/luna64-track-b-r4.3-pilot-20261010` resolved to
  that commit when checked.
- This execution handoff is a later documentation-only commit on the same
  experimental branch; `result_commit` above identifies the exact code and
  pilot artifacts.
- Required next step: independent Luna-0 review/reproduction against the
  committed input bytes, protocol, output digests, hashes, counters, resource
  evidence, and Luna-63C boundary.
- Unresolved: feasibility has been measured only for this bounded pilot.
  Scientific efficacy, future efficacy sample size/power, and any
  architecture decision remain unassessed and require separate governance
  authorization. No pilot outcome may be used to tune thresholds or pooled
  into future efficacy data.
