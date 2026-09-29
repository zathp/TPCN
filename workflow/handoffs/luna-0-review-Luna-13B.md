# Luna-0 Independent Review of Luna-13B

## Review status

`PASS — LUNA-13B CAUSAL STRUCTURAL CROSSOVER INDEPENDENTLY VERIFIED`

Luna-13C is not authorized by this review.

## Provenance

- Reviewed implementation/artifact revision: `816929fa097e049ce7d82a1f7c63fb9cc4e8bd3f`
- Branch: `main`
- Review start: clean worktree, `HEAD == origin/main`
- Contract: `.github/agents/luna-13b.agent.md`
- Execution handoff: `workflow/handoffs/causal-local-temporal-crossover-Luna-13B.md`
- Artifacts: `artifacts/causal-local-temporal-crossover-13b/results.json` and `summary.json`
- Fixture: `luna-13b-runtime-local-crossover-v1`
- CPU environment: Windows, Python 3.10.8

## Independent attack table

| Area | Independent attack | Result | Status | Limitation |
| --- | --- | --- | --- | --- |
| Causal-local evidence | Traced stimulus event through topology, neuron residual, score, controller and mutation | Runtime timestamps, elapsed intervals, residuals and decision times agree; no future/global/label input found | passed | Controlled finite-delay fixture, not task learning |
| Analytic crossover | Re-derived `score = abs(residual) * exp(-mu * elapsed)` | `mu* = 0.07833747196936626`, matching artifact | passed | Frozen fixture only |
| One-slot competition | Inspected topology/controller and reran capacity records | Two valid candidates, one remaining slot, loser rejected `edge_capacity` | passed | Small fixture |
| Structural crossover | Reran low/high conditions | `right -> target` versus `left -> target`; final edge sets differ | passed | No external task target |
| Relabeling | Used `z_candidate` and `a_candidate` identifiers | Evidence-bearing role selected `z_candidate` | passed | Two-candidate fixture |
| Mirroring | Reversed semantic role mapping while preserving role evidence | Semantic winner remained the expected role; identifier changed | passed | Mirror is fixture-level |
| Ties | Replayed explicit exact tie and analytic near-boundary condition | Identifier tie rule deterministic; near-boundary selection reproducible | passed | Exact tie control is explicit; floating-point near tie is separate |
| Negative controls | Reran reversed, shuffled, uniform, neutral, random, score-shuffled and fixed controls | Each altered or removed the declared evidence-to-growth behavior | passed | Deterministic controls are not statistical replication |
| Scoring vs execution decay | Held execution decay fixed across primary crossover; varied execution decay independently | Scoring parameter changes primary winner; execution parameter remains separately configurable | passed | No claim that runtime decay is irrelevant |
| Bounded execution | Inspected counters and raised budget from 12 to 30 | Primary/control runs completed; 7 processed, 0 pending, no exhaustion; extended budget unchanged | passed | CPU reference only |
| Deterministic replay | Repeated primary, near-tie and future-probe conditions | Evidence, scores, ranks, edges and termination reproduce | passed | Random control uses declared seed, not replication |
| Provenance | Compared artifact metadata with checked-out implementation and regenerated representative results | Revisions/configuration/environment match recorded execution | passed | Artifact records clean state before generation, not a VCS attestation |
| Stage-0 regressions | Ran invariant/runtime/structural/reward slice and full CPU suite | Review slice `135 passed`; full suite `250 passed, 1 skipped` | passed | Optional CUDA skip not applicable |
| Architecture interpretation | Checked A01-A08, A11, A14, A15 boundaries and no core edits | No contract amendment or architecture promotion | passed | No hardware equivalence claim |
| Workflow update | Added this handoff, workflow result and changelog entry | Authoritative records now contain review outcome and authorization boundary | passed | Publication commit is separate from reviewed implementation |

## OBSERVED

The primary low condition produced scores `(left=0.6333861926251716,
right=0.7408182206817179)` and admitted `right -> target`. The high condition
produced `(left=0.5185727544772024, right=0.4065696597405991)` and admitted
`left -> target`. Both began with zero edges and one remaining edge slot; the
loser was rejected for `edge_capacity`. Their explicit final edge sets and
graph fingerprints differed.

Each candidate record came from a runtime stimulus event followed by a routed
target event. The recorded observation timestamp was no later than the local
decision timestamp. Scores used the canonical neuron's local residual and the
configured scoring decay. A future target probe and a larger event budget did
not change candidate evidence or structural output.

The frozen equality point was independently reproduced. Reversed and shuffled
controls generated no ordered association records; fixed topology generated no
edge; uniform and neutral conditions removed the candidate-specific decay
distinction; score-shuffled selection changed the structural choice while
preserving the raw score ranking.

## INFERRED

Within this bounded CPU fixture, the evidence supports the narrow causal chain
`runtime-local observation -> decay-sensitive score -> rank reversal ->
one-slot admission reversal -> final graph reversal`. The finite interval
configuration is a controlled runtime stimulus, not a claim of online task
learning or general temporal superiority.

## HYPOTHESIZED

A learned structural edge may have a useful causal effect in an external task,
but that question was not tested here. It requires a separately authorized
experiment with edge-present, targeted-edge-removed, restored, sham, unused-
edge, fixed-useful-edge, fixed-topology and equal-budget random-growth
comparisons.

## Validation record

| Command | Result |
| --- | --- |
| Independent primary/control attack script | passed |
| Focused Luna-13B and preservation slice | `135 passed` |
| Full CPU suite | `250 passed, 1 skipped` |
| `python -m compileall -q tpcn tests run_temporal_crossover.py` | passed |
| Standard diagnostics on touched Python files | no errors |
| `git diff --check` | passed |
| CUDA/GPU validation | not applicable to CPU-only review |

## Remaining limitations and boundary

This result does not establish task usefulness, classification or external
prediction improvement, energy efficiency, scalable benefit, superiority over
fixed/random learning, hardware equivalence or biological plausibility. The
known Luna-12J manual replay termination-status issue remains non-gating and
was not silently promoted. No Luna-13C agent contract was created or
executed. A future causal-usefulness target is eligible for a new contract
proposal only after an explicit project-owner request and normal Luna-0 review.
