# Luna-0 Final Closure Handoff: Luna-13F

**NEGATIVE RESULT - LUNA-13F RUNTIME EVIDENCE DOES NOT PREDICT USEFUL GROWTH, INDEPENDENTLY VERIFIED AND CLOSED**

```yaml
tpcn_handoff:
  agent: Luna-0
  luna_identifier: "Luna-13F final closure review"
  descriptive_name: "Independent closure of runtime-generated local candidate evidence"
  task_id: luna-0-final-closure-review-runtime-generated-local-candidate-evidence-13f-closed
  component: "Luna-13F CPU fixture, runtime controls, artifacts and governance"
  status: complete
  contract_version: "1.1"
  branch: main
  base_revision: 83266f92d750939ef0b9904073e9f75badc35fbb
  result_revision: "pending publication"
  implementation_revision_reviewed: 83266f92d750939ef0b9904073e9f75badc35fbb
  artifact_generating_revision: 83266f92d750939ef0b9904073e9f75badc35fbb
  worktree_at_review_start: clean
  head_equals_origin_main_at_review_start: true
  architecture_change: false
  proposal: null
  luna_13g: unauthorized
```

## Closure Result

| Area | Final result |
|---|---|
| P0 | `candidate_A`, `2/2`; candidate A maps to relay |
| P1 | `candidate_A`, `1/2`; candidate A maps to noise |
| Blinding | PASS: neutral candidate identities and endpoint mappings precede held-out evaluation; no role, label, utility or expected-winner input |
| Evidence provenance | PASS: runtime event observations, source-local policy/neuron state and bounded score updates precede admission |
| Evidence mechanism | PASS: bounded source-local temporal-association counts; primary scores `4.0` and `0.0` |
| Scorer | PASS: unchanged `StructuralPlasticityController`; score/rank/selection are canonical and order-independent |
| One-slot competition | PASS: both candidates individually legal; two existing edges leave one relevant slot; loser is rejected by edge capacity |
| Future continuation | PASS: same runtime processed 10 post-admission events; losing/live evidence changed `0.0 -> 5.0` |
| Historical-decision immutability | PASS: frozen evidence, scores, rank, selected candidate, topology and decision timestamp remained unchanged |
| Chronology-before | PASS: queued held-out event executed before admission and invalidated the trial |
| Chronology-equal | PASS: equal-time queue sequence executed before admission and invalidated the trial |
| Chronology-after | PASS: strictly later event executed after structural admission and was valid held-out evaluation |
| Locality cross-candidate | PASS: mutating real candidate-B private score state to `999` left candidate-A raw evidence at `4.0`; prohibited inputs read: none |
| Label isolation | PASS: external label/result mutation left pre-admission schedule, evidence, score, rank, selection and topology unchanged |
| Candidate bounds | PASS: maximum two candidates, history eight, score bound eight, deterministic full-capacity rejection |
| Reset/stale reuse | PASS: reset clears history/scores/counters; reused candidate score is clean and does not inherit stale state |
| Budget boundary | PASS: below threshold incomplete/no valid admission; threshold completes; larger budgets preserve score and selection |
| Mirroring | PASS: mirrored runtime motif moves preference and selection to candidate B |
| Equalization | PASS: equivalent runtime exposure produces equal evidence/scores |
| No evidence | PASS: removing informative exposure produces zero-score tie; any selection is deterministic tie-breaking only |
| Audit | `26 PASS / 0 FAIL / 2 valid N/A`; all 28 entries executed or explicitly conditional |
| N/A expiry | VALID N/A: canonical policy has no expiry mechanism; expiry condition is not implemented or required |
| N/A eviction | VALID N/A: full capacity deterministically rejects; eviction is not required by the canonical policy |
| No-growth | `2/2`, 8 processed events, proxy energy `8.0` |
| Resource result | No resource benefit established; selected P0 growth is also `2/2` but costs 12 events and proxy `12.0` |
| Proposition 1 | **SUPPORTED IN TESTED FIXTURE** |
| Proposition 2 | **SUPPORTED IN TESTED FIXTURE** |
| Proposition 3 | **NOT SUPPORTED** |
| Architecture change | `NO A01-A15 CHANGE REQUIRED`; `NO ACP REQUIRED` |
| Luna-13F closure | `LUNA-13F CLOSED - SUCCESSOR NOT AUTHORIZED` |

## Independent Findings

**OBSERVED:** P0 and P1 reproduce from the committed implementation. The
higher evidence follows the neutral short source-local association motif, not
the held-out task outcome. Neutral decay changes local neuron state but does
not change score magnitude, rank or selection; the evidence is therefore not
characterized as decay-sensitive utility prediction.

**OBSERVED:** Future, chronology and locality attacks execute through actual
runtime state and queue processing. The future continuation changes live state
while preserving the completed historical decision. Before/equal chronology
injections are rejected as pre-admission leakage, while the strictly later
injection is valid. Candidate-B private-state mutation does not alter
candidate-A evidence.

**INFERRED:** Runtime activity generates bounded local evidence and that
evidence affects canonical admission in this fixture. Across the blinded
mappings, it does not reliably predict held-out useful growth.

No replacement mechanism is inferred or authorized. Luna-13G remains
unauthorized.

## Validation Record

| Command or procedure | Result |
|---|---|
| `git fetch origin`; branch/HEAD/tree/worktree checks | `main`; implementation `83266f9`; `HEAD == origin/main`; clean at review start |
| Regenerate representative artifact at reviewed revision | P0 `candidate_A`, scores `4.0/0.0`; P0 `2/2`; P1 `1/2`; current provenance recorded |
| `python -m pytest tests/test_luna13f_runtime_generated_evidence.py -q` | `15 passed` |
| Independent repaired-control execution | Future, chronology, locality, lifecycle, budget and label controls passed |
| Preservation matrix: Luna-13E/13D/13C/13B/12H/12N/11 | `72 passed` |
| `python -m pytest -q` | `291 passed, 1 skipped` |
| `python -m compileall -q tpcn run_runtime_generated_evidence_13f.py tests` | passed |
| Diagnostics on touched runtime, runner and focused test | no errors found |
| `git diff --check` | passed |
| CUDA/GPU/FPGA/FPAA/hardware equivalence | not applicable; out of scope and non-gating |

## Artifact and Governance State

The committed artifact directory is `artifacts/runtime-generated-local-evidence-13f`.
Its `results.json`, `summary.json` and `audit-results.json` agree on the
terminal negative result, P0/P1, source-local count mechanism, controls,
lifecycle, budget, audit totals and uncalibrated `activity-cost-proxy` units.
The prior blocked closure handoff remains historical; this handoff supersedes
it as the final disposition.

A01-A15 are unchanged. No ACP, successor mechanism, expiry implementation,
eviction implementation or Luna-13G authorization was created.

## Reproduction and Next Boundary

From a clean checkout at `83266f92d750939ef0b9904073e9f75badc35fbb`, run:

```text
python -m pytest tests/test_luna13f_runtime_generated_evidence.py -q
python run_runtime_generated_evidence_13f.py --baseline-revision 83266f92d750939ef0b9904073e9f75badc35fbb --executed-revision 83266f92d750939ef0b9904073e9f75badc35fbb --output-dir artifacts/runtime-generated-local-evidence-13f
python -m pytest -q
```

The safe restoration point is the reviewed implementation revision above.
The next assignment is a separate project-owner decision; no Luna role is
authorized by this closure.
