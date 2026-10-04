# Luna-0 governance decision — post-Luna-31 Luna-12L / spiral policy compatibility

```yaml
tpcn_handoff:
  agent: Luna-0
  task_id: "luna-0-post-luna31-luna12l-spiral-policy-compatibility-decision-20261004"
  contract_version: "1.2"
  status: "complete"
  branch: main
  base_revision: "392ce2510660221d7486a59f184a1eeba6f17634"
  architecture_change: false
  proposal: null
  terminal_verdict: "PASS — HISTORICAL LUNA-12L / SPIRAL MODEL COMPATIBILITY CLASSIFIED; LUNA-32 AUTHORIZED / NOT EXECUTED"
```

## Starting state
`main`, `HEAD == origin/main == 392ce25` (`docs: close Luna-31 observable compatibility`), clean. Luna-28/29/30/31 closed; Contract 1.2, ACP-0007 accepted; E2 pruning and N3 unauthorized.

## Nine-failure reproduction
`pytest tests/test_luna12l_temporal_scale.py tests/test_spiral_benchmark.py`: 9 failed, 9 passed. All nine first-fail at `ValueError: structural plasticity is unavailable unless structural observation is enabled` (`ExperimentConfig.__post_init__`): Luna-12L `test_scale_runner_retains_all_policies_and_causal_evidence`, `test_requested_policy_is_executed_by_classifier[baseline|random|temporal|reversed]`, `test_policy_changes_classifier_execution_state`, `test_policy_scale_cross_product_preserves_provenance_and_serialization`, `test_condition_fails_on_classifier_provenance_mismatch`; spiral `test_control_results_are_deterministic_and_include_required_order_controls`.

## Current ExperimentConfig contract
`structural_policy` syntactically accepts fixed/baseline/random/temporal/reversed/e2_local_temporal, but `neuron_model="EXCURSION_V1"` (the default) with `structural_plasticity=True` requires `structural_observation=True`, `structural_policy="e2_local_temporal"` and the explicit ACP-0007 bounds. Legacy policy names are unsupported in E2. The legacy policies are exercised only by `ExperimentRunner._adapt_topology` under `TANH_LEGACY` (baseline: next node; temporal: index+2; reversed: previous node; random: seeded choice).

## Historical lineage
`tpcn/temporal_scale.py` (`06f74e4`) and `tpcn/spiral_benchmark.py` (`3b2b032`) predate E2 integration (`a206f2e`, `ac321ab`); the only neuron model then was the legacy tanh model, so the model was implicit. Default switched underneath them.

## Historical corrected Luna-12L verdict (comparison target, immutable)
Corrected primary gate **NOT SUPPORTED**; pre-coupling artifact invalid/superseded. Implicit model: legacy tanh (= `TANH_LEGACY`). Mean accuracy 0.300 reference (fixed/baseline/temporal/reversed; random 0.250), 0.225 expanded all policies; order control matched selected accuracy; reference temporal shortcut 5/5 vs none for others, but at expanded scale baseline/reversed also 5/5 (policy distinction did not survive); classifier proxy energy 48.103 fixed vs 51.467 temporal (reference), 48.923 vs 51.231 (expanded); learned-edge intervention changed routed computation; limitations: prediction loss exposed as zero, cost attribution unavailable, proxy energy uncalibrated.

## Five-policy matrix
| Policy | Historical meaning / model | Valid in current E2 | E2 equivalent | Exact equivalent | Exercised by ExperimentRunner | By run_temporal_capacity | Explicit TANH preserves | Mapping to e2_local_temporal | Disposition |
|---|---|---|---|---|---|---|---|---|---|
| fixed | no plasticity; legacy | yes (plasticity off) | none needed | n/a | yes (no growth) | yes | yes | not needed | keep, same model as others |
| baseline | next-node growth; TANH | no | none | no | yes (TANH only) | yes (capacity model) | yes | changes meaning | explicit TANH |
| random | seeded random destination; TANH | no | none | no | yes (TANH only) | yes | yes | changes meaning | explicit TANH |
| temporal | index+2 destination; TANH | no | not an alias of e2_local_temporal | no | yes (TANH only) | yes (12I-style capacity policy) | yes | changes meaning | explicit TANH |
| reversed | previous-node growth; TANH | no | none | no | yes (TANH only) | yes | yes | changes meaning | explicit TANH |

## Classifier versus temporal-capacity ownership
`run_luna12l_condition` composes two systems: `run_temporal_capacity(policy, ...)` supplies structural edge/path/mutation/intervention metrics, and `_classification_metrics` runs the classifier through `ExperimentRunner` with the same policy name. The historical corrected design intentionally pairs them (named policy and scale carried through `ExperimentConfig`; classifier metrics from the classifier run; structural metrics from the matching capacity run). They are different implementations sharing a policy string and are not equivalent.

## Requested/executed provenance
`executed_policy = policy` is a echo of the requested string, backed by real execution only when the legacy runner executes that policy. Under E2 it would be false provenance; under explicit `TANH_LEGACY` the requested policy genuinely reaches `_adapt_topology`. Probe: config digests, classifier topology edges and edge counts differ by policy (e.g. reference baseline 2 edges/digest 2eb7c30b vs temporal digest ba822e9f); reference and expanded stay distinct; the deliberate mismatch reaches `RuntimeError: classifier condition provenance does not match requested condition`.

## Explicit TANH compatibility probe (diagnostic only, not evidence)
All 10 scale/policy conditions execute with all five conditions on one model; no cross-model mixing. Versus the retained artifact (seeds 0-2, 30 conditions): event counts 30/30 and classifier topology edges 30/30 match; proxy energy 0/30, replay digests 0/30 and accuracy 23/30 match (current legacy code and config differ from 12L-time code; config digest also changed with new config fields). **Conclusion: NOT THE SAME EXPERIMENT**; historical evidence stays frozen.

## Cross-model confound / ACP-0007 reinterpretation
Rejected: `fixed` on E2 with the other four on TANH (policy confounded with model). Option B (fixed E2, e2_local_temporal, order-destroyed controls, etc.) is a **NEW EXCURSION_V1 / ACP-0007 four-class experiment** requiring its own contract; it is not compatibility, and it is not authorized here. No fake aliases to e2_local_temporal.

## Spiral
`run_controls()` (ten controls, one base config, seed 17) is a matched single-model benchmark authored under the legacy model. Probe: with all controls on `TANH_LEGACY`, `run_controls` executes and `first == second`; the structural control grows (4 mutations). Making only the structural control TANH would make the structural comparison a model comparison (fixed controls 1 edge vs structural 2) — rejected. The current-E2 alternative needs a full ACP-0007 profile and would be a new benchmark, not compatibility. Decision: spiral is a historical consumer, the same mechanism applies, and it is included in Luna-32 with a separate acceptance item.

## Test classification
| Test | Invariant | Disposition |
|---|---|---|
| scale_runner_retains_all_policies_and_causal_evidence | historical preservation, causal evidence | MIGRATE TO EXPLICIT LEGACY |
| requested_policy_is_executed_by_classifier x4 | policy provenance | MIGRATE TO EXPLICIT LEGACY (genuine execution; no string echo) |
| policy_changes_classifier_execution_state | historical topology dependence | MIGRATE TO EXPLICIT LEGACY |
| policy_scale_cross_product_preserves_provenance_and_serialization | provenance, scale, serialization | MIGRATE TO EXPLICIT LEGACY |
| condition_fails_on_classifier_provenance_mismatch | provenance guard | MIGRATE TO EXPLICIT LEGACY (valid condition runs far enough to hit RuntimeError) |
| spiral control_results_are_deterministic_... | determinism, matched controls | MIGRATE TO EXPLICIT LEGACY (all ten controls one model) |
None removed, replaced by E2 oracles, or retagged as new evidence. Scales stay historical.

## Architecture audit
A01 no timing change; A03/A04 routing/topology finite and existing; A06 prediction semantics unchanged; A07 labels external to structural evidence; A08 determinism/bounds preserved (spiral first==second); A10 proxy energy diagnostic; A14 ACP-0007 E2 growth unchanged; A15 software experiment only. All PASS for the planned scope. Architecture/ACP change: NO / NO.

## Decisions
- Historical compatibility possible: **yes**
- New E2 experiment required: **no for this compatibility task; yes (separately, not authorized) to answer what current ACP-0007 shows**
- Luna-32 authorized: **yes** — `Luna-32 — Historical Luna-12L / Spiral Model-Explicit Compatibility`, `.github/agents/luna-32.agent.md`; sequence Luna-0 -> Luna-32 -> Luna-0, not executed
- Owned: `tpcn/temporal_scale.py`, `tpcn/spiral_benchmark.py`, `tests/test_luna12l_temporal_scale.py`, `tests/test_spiral_benchmark.py`, `workflow/handoffs/luna-32-historical-temporal-spiral-model-compatibility-20261004.md`
- Prohibited: experiments/E2 runtime/excursion neuron/structural observation/temporal association/structural plasticity/topology/visualization sources, run scripts, `artifacts/`, ACP-0007, Contract, other tests
- Spiral included: **yes**
- Remaining groups until Luna-32: 8 Luna-12L, 1 spiral. Luna-33 not authorized.

## Terminal verdict
PASS — HISTORICAL LUNA-12L / SPIRAL MODEL COMPATIBILITY CLASSIFIED; LUNA-32 AUTHORIZED / NOT EXECUTED
