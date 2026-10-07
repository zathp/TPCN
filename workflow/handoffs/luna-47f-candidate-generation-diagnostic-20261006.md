---
tpcn_handoff:
  agent: "Luna-47F implementation worker"
  luna_identifier: "Luna-47F"
  descriptive_name: "Fan-In / Shortcut Candidate-Generation Diagnostic"
  task_id: "luna-47f-candidate-generation-diagnostic-20261006"
  component: "Downstream retained-trace replay only"
  status: "complete - PARTIALLY SUPPORTED for proxy opportunities; independent review pending"
  contract_version: "1.2"
  branch: "copilot/luna47f-investigation"
  base_revision: "789dda5988daf72f375d9713bd76a6da2b9e8b34"
  production_evidence_baseline: "2cef8ea4b37a4ae586e3f383511cba63c9268ddc"
  protocol_revision: "8af8d733a1c8fc7762ef3e34bec775afc10ca2ae"
  execution_revision: "39f99b1f318dd965643ec6ef65907163cd1d5667"
  result_revision: "Publication commit containing this handoff; exact hash returned in final report"
  dependencies:
    - "Committed Luna-47F contract and Luna-0 common authorization"
    - "Reviewed Luna-44 fixture/provenance and Luna-45 calibrated initial/replay observations"
    - "Luna-46 corrected output and MIXED independent review"
    - "Applicable Luna-12I/J/K/M/N handoffs and retained historical controls, interpretation only"
  owner: "Project owner; independent review by Luna-0"
  classification: ["REPLAY ONLY", "MECHANISM DIAGNOSTIC", "PARTIALLY SUPPORTED", "NO EFFICACY"]
  hypothesis: "Compatible earlier-to-later causal deltas offer nonduplicate shortening/fan-in proposals before mutation."
  counter_hypothesis: "Only existing routes, incompatible deltas, nonlocal information, or no useful downstream activity are observed."
  interfaces_relied_on:
    - "Retained JSON emission, enqueue, reception, integration trace and trigger-check fields"
    - "Immutable retained topology/resource configuration; no production imports"
  label_information_boundary:
    - "No class labels, rewards, audit x+y or downstream utility enter scoring."
    - "Later target emissions are evaluation-only associations, never candidate inputs."
  timing_assumptions:
    - "Retained logical time; exact identities/copied times/bits; 0 < lag <= 4.0."
    - "Same-sign nonzero scalar similarity min(abs)/max(abs) >= 0.5; no boundary tolerance."
    - "Equation bound: 64 binary64 epsilons times max(1, magnitudes)."
  reset_boundaries:
    - "All observation and repeated-proposal accounting resets per stream and rule family."
    - "Static graph never changes; no hypothetical proposal consumes capacity."
  resource_bounds:
    - "320 streams; maximum 4096 routed observations per stream; maximum 100 MiB per source file."
    - "Fixed three nodes, two edges; fan-in/out limits 2, edge/routing capacities 3."
    - "2420 bounded output rows; no production state or counterfactual execution."
  authorized_scope:
    - "Read retained evidence, predeclare scoring rules, replay and classify opportunities."
    - "Own only experiments/luna47f, artifacts/luna47f, tests/test_luna47f_*.py and this handoff."
    - "Commit code/protocol before outcomes; publish isolated branch and stop."
  unauthorized_scope:
    - "No edge creation/removal/admission/reprioritization, production/topology/governance edit, ACP or architecture change."
    - "No task efficacy, counterfactual production run, hardware equivalence, merge, successor or delegation."
  controls:
    - "Exact retained initial/replay canonical analysis equality."
    - "Direct route duplicates separated from exact two-hop trigger chains."
    - "Separate local-deposition deltas versus explicitly labeled output-drive proxies."
    - "Compatible same-stream nontrigger coincidences, (4,8] lag band and reverse-order exclusions."
    - "Synthetic unit fixtures are tests only, never retained evidence."
  measurements:
    - "Opportunity rows/times/endpoints/causal chains/similarity, repeated and static duplicates, cycles and saturation."
    - "Analytical hop shortening and fan-in opportunities, not created edges or delay savings."
    - "Actual target deposition versus exact trigger-linked canonical emission associations."
    - "12 consumed source identities and 878 protected non-owned pre/post working-byte hashes."
  information_boundary_check:
    - "PASS downstream-only evaluation; no output enters TPCN computation."
    - "BLOCKED deployable source-local evidence: no retained return channel for downstream observations."
  hardware_mapping:
    - "Not evaluated; no hardware units or equivalence claim."
  architecture_invariants_touched: ["A01", "A02", "A03", "A04", "A07", "A08", "A14"]
  preserves:
    - "Luna-46 MIXED; all reviewed source provenance and negative results"
    - "ACP-0007 disabled/unchanged; ACP-0008 experimental, opt-in and unpromoted"
    - "All production, topology, fixtures, governance and other lane files unchanged"
  architecture_change: false
  proposal: null
  files_changed:
    - "experiments/luna47f/PROTOCOL.md"
    - "experiments/luna47f/diagnostic.py"
    - "experiments/luna47f/README.md"
    - "tests/test_luna47f_diagnostic.py"
    - "tests/test_luna47f_retained.py"
    - "artifacts/luna47f/diagnostic.json"
    - "artifacts/luna47f/validation.json"
    - "workflow/handoffs/luna-47f-candidate-generation-diagnostic-20261006.md"
  tests_added:
    - "50 synthetic/unit checks: compatibility/window, direction, duplicate/cycle/saturation, capacity absence, identity failures, exact newline materialization and non-mutation"
    - "5 retained checks: hashes/replay, exact JSON-pointer reconciliation, blocked boundaries, family totals and read-only CLI reproduction"
  tests_passing:
    - "Focused: 55 passed; 38.91 seconds."
    - "Applicable regression: 373 passed, but selected suite failed."
    - "py_compile and git diff --check passed."
  tests_failed:
    - "Applicable regression: 2 failed and 7 setup errors; no failures suppressed."
    - "Luna-44 pinned-source materialization failure and seven verification setup errors."
    - "Luna-46 retained-artifact integrity test rejects checkout CRLF catalog hash."
  tests_not_run:
    - "Full repository suite; independent Luna-0 review."
    - "No production/counterfactual/efficacy/hardware experiment."
  assumptions:
    - "Exact trigger linkage proves a causal trigger, not exclusive or complete contributing ancestry."
    - "Output drive and deposition have comparable scalar units but are not intrinsic source-state deltas."
    - "Capacity opportunity is evaluated against static recorded limits, not an admission decision."
  unresolved:
    - "Source intrinsic state-delta compatibility, source-local observation delivery, usable edge, proposed delay and task utility are BLOCKED."
    - "Cross-platform/materialization parity and Windows fixture regressions remain unresolved."
    - "Independent Luna-0 review pending; no promotion or follow-up authorization."
  recommended_next_agent:
    - "Independent Luna-0 review only; no successor implementation."
---

# Luna-47F completed replay-only diagnostic

## Outcome and owned scope

**OBSERVED:** Verdict **PARTIALLY SUPPORTED**, strictly for
output-drive-proxy geometric opportunities. The stronger intrinsic/local/useful
candidate-generation hypothesis is **not established**. No edge was created,
removed, admitted, ranked or used in a counterfactual production run.

The baseline is the exact common documentation-only authorization revision
`789dda5988daf72f375d9713bd76a6da2b9e8b34`, descended from production/evidence
baseline `2cef8ea4b37a4ae586e3f383511cba63c9268ddc`. Protocol, code and synthetic
tests were committed at `8af8d73` before outcome artifacts. The first invocation
stopped before scoring/output at the source-byte gate: this Windows checkout
materialized Luna-45's LF JSON with CRLF. A provenance-only correction was tested
and committed at `39f99b1` before the successful scoring invocation. **No scoring
rule or source file changed.** The correction reads published baseline Git bytes,
requires exact working bytes or their exact Git LF-to-CRLF transform, and records
both hashes/lengths. Catalog and internal digests are checked on published bytes.

The scope contains only the eight listed files. No production, edge, fixture,
shared workflow, architecture or another lane's file changed. There was no
delegation, merge or consumption of another lane's unreviewed results.

## Retained evidence and predeclared rules

**OBSERVED:** 320 retained calibrated Luna-45 streams; 1,950 actual route
enqueue/reception pairs per phase, comprising 1,715 source→relay and 235
relay→destination pairs. All pairs reconcile by exact stream/event/queue identity,
endpoints, route path, payload bits, copied times and bounded root metadata.
Each direct route matches its actual emission and declared finite delay; input
deposition equations match under the declared 64-epsilon bound.

The temporal rule is `0 < lag <= 4.0` retained logical-time units (Luna-45's
precursor window). Similarity is same-sign, nonzero
`min(abs(delta_a),abs(delta_b))/max(abs(delta_a),abs(delta_b)) >= 0.5`.
No threshold/window tolerance or optimized sweep was used. Character streams
and rule families are independent reset scopes.

Two distinct evidence families are retained:

- **Local deposition:** relay reception `input_value` and destination reception
  `input_value`, verified against `x_after_input-x_after_decay`. These isolate
  local event deposition rather than conflating decay/discharge with net change.
- **Output-drive proxy:** earlier canonical signed emission payload against later
  event deposition. This is explicitly **not intrinsic source-state-delta
  compatibility**; source pre/post update fields are missing.

Two-hop identity is destination receipt → actual relay emission → exact
relay integration trigger → actual source→relay receipt → source emission.
Every row includes exact JSON pointers, event/node/stream IDs, timestamps,
delta values, similarity, classifications and chain. Five route pairs carry
`roots_truncated=true`; these are preserved bounded-root flags, not missing
captures. Exact trigger linkage does not reconstruct full ancestry.

Historical Luna-12K shortcut intervention and Luna-12M/12N candidate/control
evidence remain context only. Their synthetic/historical model results are not
pooled into EXCURSION_V1 replay. In particular, Luna-12N's score/rank change was
not an admitted-edge-set or final-graph change, and historical synthetic
candidate evidence is not substituted for online causal observations here.

## Quantitative results

The two families overlap causal chains and **must not be pooled as independent
candidate evidence**. No delta/window rejection occurs in either family; the
chosen similarity rule does not discriminate among these enumerated routes.

| Metric | Output-drive proxy | Local deposition |
|---|---:|---:|
| Enumerated compatible in-window opportunities | 2,185 | 235 |
| Streams with opportunities | 297 | 108 |
| Unique endpoint pairs | 3 | 1 |
| Existing-edge duplicates | 1,950 | 235 |
| Repeated endpoint proposals within stream/family | 1,672 | 127 |
| Novel static-capacity-feasible opportunities | 235 | 0 |
| Analytical one-hop shortening opportunities | 235 | 0 |
| Fan-in creation opportunities, **not actual creation** | 235 | 0 |
| Cycle-forming opportunities | 0 | 0 |
| Saturated fan-in/fan-out/global-edge/routing sets | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 |
| Trigger-linked canonical target-emission associations | 235 | 0 |
| **Novel** opportunity target-emission associations | **0** | **0** |
| Compatible pairs outside window / in (4,8] | 0 / 0 | 0 / 0 |

**OBSERVED:** All 235 novel proxy rows have the **same endpoint pair**,
source→destination, across 108 streams; 127 are within-stream repetitions.
There are not 235 distinct edges. Local deposition yields only the existing
relay→destination edge. Static-edge duplicates and repeated proposals overlap.

For the novel proxy rows, similarity ranges from `0.5045597858886401` to
`0.9952492750743483`. Lag is approximately 2.5, preserving exact binary64 values
in rows (range `2.4999999999999716`–`2.5000000000000284`); candidate/observation
times range `16.885599033056476`–`322.7280569532988`. Direct-route proxy lag is
approximately 1.0 and relay→destination deposition lag approximately 1.5.

The existing source→relay→destination path has two hops and cumulative
**transport delay 2.0**, distinct from the observed 2.5 trigger-to-destination
lag, which includes relay processing/emission timing. A not-instantiated direct
edge would geometrically reduce hops by one. Its delay/delay reduction is
**BLOCKED**: no prospective edge was configured or admitted.

The frozen graph has three nodes/two edges; fan-in/out limits are 2, global
edge and routing capacities 3. Each novel row is independently feasible under
those static limits. Proposals do not consume the one spare slot; no allocation,
locality policy, admission, queue budget under added traffic or actual reachable
edge is established.

The 235 proxy target-emission associations are source→relay duplicate rows:
they associate with actual relay emissions. All novel source→destination
rows and local relay→destination rows have **zero** destination canonical
emissions. Destination deposition is observed, but is not useful task activity
or efficacy. No classification, prediction-loss, energy or utility score was run.

## Temporal specificity and meaningfulness

**OBSERVED:** Zero compatible same-stream nontrigger temporal coincidences;
zero compatible (4,8] lag-band pairs. Reversing the enumerated endpoints would
exclude all 2,185 proxy / 235 deposition pairs by strict temporal direction.
Those are algebraic direction exclusions, not alternate neural runs.

**INFERRED:** Fixed positive route delays and exact trigger selection largely
force these lag relationships. With no competing in-window nontrigger matches,
no capacity pressure and all similarity scores passing, this replay does
**not** establish statistical temporal specificity, superiority over random
growth, generalization, or useful candidate prioritization.

**BLOCKED:**

1. Source intrinsic pre/post state-delta comparison: missing source update fields.
2. Source-local observation availability: no retained downstream-observation
   delivery/return channel. Offline global linkage is not local learning.
3. Usable/reachable proposed edge: no locality/admission/intervention authorized.
4. Prospective delay reduction: no declared candidate-edge delay.
5. Task utility/efficacy: no intervention or task scoring authorized.
6. Complete ancestry: bounded roots remain incomplete where truncated.

**HYPOTHESIZED:** The repeated proxy endpoint is a possible question for
independent review, not a recommendation to add it. Count-only positivity
cannot establish efficacy. The predeclared SUPPORTED gate additionally requires
novel target-emission association and source-local availability; neither is met.
The limited geometric proxy gate alone yields **PARTIALLY SUPPORTED**.

## Non-mutation and architecture evidence

**OBSERVED:** All **878 non-owned tracked files** have equal pre/post SHA-256
values, individually retained in `diagnostic.json#/non_mutation`.
Aggregate snapshot digest:
`92c24063e6865e07b81047f93a7a3ba74d7473d05ccd7bd6598528bfa6aca6c9`.
This includes all topology source/artifacts, fixtures and retained evidence.
The later focused read-only CLI check also verifies these hashes after the
regression run. The non-owned Git diff against authorization is empty.

The canonical analytical result hash is
`c769d0eb052f4797e38f46591d38623613202ee9c391283e11cbd08162ae6bdf`;
initial/replay canonical bytes match exactly. Twelve consumed source identities
retain baseline Git blobs, published and working byte SHA-256/lengths,
materialization classification and complete retained configuration/provenance.

| Clause | Evidence |
|---|---|
| A01-A02 | Retained event times; no global tick or neural execution; per-stream reset |
| A03 | Exact emission/enqueue/reception chains; finite existing route delay; no instantaneous candidate route |
| A04 | Static recorded capacities classified, not mutated or consumed |
| A07 | Downstream-only global analysis; source-local availability explicitly BLOCKED |
| A08 | Finite input/row bounds; cycle classifications unit-tested; no recurrent execution |
| A14 | Opportunities, duplicates, capacity limits and unavailable admissions distinguished |

Luna-46 remains **MIXED**. Its corrected output is read/pinned, not recomputed,
rewritten or reinterpreted. Luna-45 **NOT SUPPORTED IN THIS SETUP** and other
reviewed predecessor negatives are not promoted. ACP-0007 and ACP-0008,
architecture A01-A15 and all governance documents remain unchanged.

## Validation record and retained negatives

Full commands/environment/results/failing names are machine-readable in
`artifacts/luna47f/validation.json`.

| Procedure | Observed result |
|---|---|
| Pre-outcome synthetic checks, protocol commit | 49 passed |
| Provenance-only correction synthetic checks | 50 passed |
| Committed retained initial/replay diagnostic | PARTIALLY SUPPORTED; byte-identical analytical results |
| Focused unit + retained tests | **55 passed**, including read-only reproduction and row-pointer reconciliation |
| Final focused recheck after regressions, strengthened scalar/similarity assertions | **55 passed**, 23.98 seconds; protected hashes still identical |
| Applicable 12I/J/K/M/N, 38, 44 fixture/verifier, 45, 46, runtime/topology/plasticity regressions | **373 passed, 2 failed, 7 errors; exit 1** |
| `py_compile` and `git diff --check` | PASS |
| Full repository suite | Not run |
| Independent Luna-0 review | Pending |

No selected-suite failure is waived:

- Luna-44's committed-fixture materialization test fails with a pinned-source
  worker subprocess exit 1. Seven Luna-44 verifier tests error during the same
  module setup materialization. This is consistent with the already documented
  Windows pinned-source LF/CRLF limitation; no fixture generator/test expectation
  was changed or bypassed.
- `test_real_retained_artifacts_integrity_only` in Luna-46 additionally fails
  with `Blocked: published Luna45 catalog hash differs`. Published catalog
  SHA-256 is `a47046da6916db49f373613d654d2cf59671737b5c6b8584b222fb67fe068e8e`;
  the unchanged working CRLF materialization is
  `5c41184dc9b9b5872263bcbbc1e5fc406789101c27942480b9cfb6b33c87da80`.
  The exact newline-only relationship was verified. This observed failure is
  recorded separately, not misrepresented as the earlier generator signature.

The regression source/test files are identical to authorization; the lane does
not repair these out-of-scope materialization problems. Selected-suite status
remains **FAILED**, despite focused diagnostic success.
VS Code test discovery/Pylance syntax lookup did not resolve this isolated
worktree; direct pytest/py_compile were used. The Problems tool reported no
errors for owned files, but no full static-analysis claim is made.

## Reproduction, rollback and review boundary

From the specified isolated worktree, with the recorded Python 3.11.5 interpreter:

```powershell
Set-Location 'C:\Users\zathp\.copilot\session-state\2c38ab9f-63a7-41fb-8437-e11b4732bee9\files\luna47f'
& 'C:\Users\zathp\Documents\programming\TPCN\.venv\Scripts\python.exe' experiments/luna47f/diagnostic.py --check
& 'C:\Users\zathp\Documents\programming\TPCN\.venv\Scripts\python.exe' -m pytest -q tests/test_luna47f_diagnostic.py tests/test_luna47f_retained.py
```

The fixed published output is never overwritten. `--check` is read-only,
recomputes both retained phases, and checks analysis, source, code and protected
hashes. Original generation without `--check` requires an absent lane output.
Exact working-byte/code hashes bind the original materialization; other checkout
policies or platforms may fail strict identity checks. Cross-platform parity is
unproven. Symlink/reparse output components are rejected, but concurrent alias
replacement races are not claimed eliminated.

Rollback is simply not integrating this isolated lane, or reverting its owned
commits; nothing in production/topology needs restoration. Commit messages carry
the requested Copilot co-author trailer. Publication commit/ref parity is verified
after this handoff is committed and pushed; exact commit hashes are returned in
the final report.

**Next assignment:** independent Luna-0 review only, receiving this handoff,
protocol/code/tests, source inventory, all rows and failed validation gates.
No architecture promotion, merge, graph change or successor (including Luna-48)
is authorized. Stop after pushing the handoff.
