# Luna-32 Historical Luna-12L / Spiral Model-Explicit Compatibility

```yaml
tpcn_handoff:
  agent: "Luna-32 Historical Luna-12L / Spiral Model-Explicit Compatibility"
  task_id: "luna-32-historical-temporal-spiral-model-compatibility-20261004"
  contract_version: "1.2"
  status: "implemented-published-awaiting-independent-review"
  branch: "main"
  authorization_source_revision: "392ce2510660221d7486a59f184a1eeba6f17634"
  authorization_publication_revision: "5696b2ff0886d589559b366e885661e5106be1dd"
  execution_starting_revision: "5696b2ff0886d589559b366e885661e5106be1dd"
  implementation_revision: "a70c8cd6df7cdbb98ef11e7a76711e5ead918cb8"
  handoff_publication_revision: "separate publication commit; exact revision is reported with the final publication result"
  final_origin_main: "verified after handoff publication; exact revision is reported with the final publication result"
  architecture_change: false
  proposal: null
  terminal_verdict: "PASS — LUNA-32 HISTORICAL LUNA-12L / SPIRAL MODEL-EXPLICIT COMPATIBILITY — READY FOR INDEPENDENT REVIEW"
```

## Scope and implementation

Luna-32 makes the historical model selection explicit. It does not conduct a
current `EXCURSION_V1` / ACP-0007 experiment and does not revise the corrected
historical Luna-12L scientific result.

The classifier `ExperimentConfig` in `tpcn/temporal_scale.py` now explicitly
sets `neuron_model="TANH_LEGACY"` for every policy, including `fixed`. The
historical `structural_plasticity = policy != "fixed"` and
`structural_policy = policy` values remain unchanged. The policy string reaches
the legacy `ExperimentRunner` adaptation path; no policy translation or
`e2_local_temporal` alias was introduced. `executed_policy` remains backed by
the actual configured execution, and the existing requested/executed
provenance guard is unchanged.

The shared base configuration in `spiral_benchmark.run_controls()` now sets
`neuron_model="TANH_LEGACY"`, so all ten controls use the same model. The
caller-owned configuration and accepted policy set of `run_policy_control()`
were not changed. The source and test modules identify these paths as a
**HISTORICAL COMPATIBILITY EXPERIMENT** and **NOT CURRENT EXCURSION_V1 /
ACP-0007 EFFICACY EVIDENCE**.

No executed-model field was added to `FourClassMetrics`: actual model use is
verified by capturing the `ExperimentConfig` passed into the classifier
runner, and the config digest already commits to that model setting.

## Files changed

- `tpcn/temporal_scale.py`
- `tpcn/spiral_benchmark.py`
- `tests/test_luna12l_temporal_scale.py`
- `tests/test_spiral_benchmark.py`
- `workflow/handoffs/luna-32-historical-temporal-spiral-model-compatibility-20261004.md`

No other file was changed. In particular, `artifacts/`, the historical
Luna-12L result handoff, ACP-0007, the Architecture Contract, core runtime,
other tests and run scripts are unchanged.

## Compatibility diagnostics

The bounded policy diagnostic ran each of the five policies at both historical
scales, captured both actual classifier configs (selected and reverse-order
control), and verified TANH_LEGACY, requested/executed policy identity,
policy-specific structural flags, deterministic config digests and classifier
edge counts.

| Scale | Policy | Config digest (prefix) | Classifier topology edges |
|---|---|---:|---:|
| reference | fixed | `b362c6e7` | 1 |
| reference | baseline | `2eb7c30b` | 2 |
| reference | random | `a7e66a30` | 2 |
| reference | temporal | `ba822e9f` | 2 |
| reference | reversed | `00ad57a6` | 2 |
| expanded | fixed | `5acc3f19` | 1 |
| expanded | baseline | `2e4600ec` | 2 |
| expanded | random | `13590560` | 2 |
| expanded | temporal | `8c62e728` | 2 |
| expanded | reversed | `77687000` | 2 |

The five requested policies each execute with `TANH_LEGACY`; `fixed` disables
plasticity while retaining `structural_policy="fixed"`, and the four historical
growth policies retain their own names and reach the real TANH legacy policy
branch. Reference and expanded configurations remain distinct. Historical
scale parameters are unchanged:

- Reference: 7 nodes, edge capacity 6, fan-in/out 2, candidate/history 8,
  queue/event 16, growth attempts 3.
- Expanded: 12 nodes, edge capacity 10, fan-in/out 3, candidate/history 12,
  queue/event 24, growth attempts 5.

The intentional provenance-mismatch test still raises
`RuntimeError: classifier condition provenance does not match requested
condition`. A separate diagnostic confirmed that a valid TANH legacy condition
executes before the deliberately mismatched `executed_policy` reaches this
guard.

For the spiral diagnostic fixture, all ten controls were captured on
`TANH_LEGACY`; repeated `run_controls()` calls returned equal results. The
small-fixture structural control reported one mutation. These are
compatibility checks only, not E2 structural-growth evidence.

## Historical evidence and scientific boundaries

The corrected historical Luna-12L verdict remains **NOT SUPPORTED**. It is
unchanged by this compatibility correction. The explicit-TANH compatibility
run is **NOT THE SAME EXPERIMENT AS THE RETAINED LUNA-12L ARTIFACT**: the
authorization probe matched event counts and classifier topology edge counts
in 30/30 artifact conditions, but proxy energy in 0/30, replay digests in 0/30,
and accuracy in 23/30. No historical result or artifact was regenerated or
overwritten. No diagnostic here is a reproduction, correction, superseding
result or new efficacy evidence.

All ten spiral controls remain a matched single-model comparison. No
cross-model policy comparison was introduced. No legacy policy was mapped to
`e2_local_temporal`.

## Verification

- Focused Luna-12L and spiral suites:
  **18 passed** (`tests/test_luna12l_temporal_scale.py`,
  `tests/test_spiral_benchmark.py`).
- Legacy and E2 regression selection:
  **96 passed** (`tests/test_experiments.py`,
  `tests/test_structural_plasticity.py`, `tests/test_topology.py`,
  `tests/test_luna28_excursion_structural_growth.py`,
  `tests/test_luna12b_integration.py`). This includes default fixed-topology
  and explicit bounded E2 structural-growth coverage. A focused runtime
  check also confirmed `ExperimentConfig().neuron_model` remains
  `EXCURSION_V1`.
- Full suite: **908 passed, 0 failed, 1 skipped** in 14.98s.
- Collection: **909 tests collected**. No tests were deleted, renamed to evade
  collection, converted to xfail, unconditionally skipped or deselected.
- CUDA skip: the unchanged
  `tests/test_gpu_visualization.py::test_cuda_records_have_cpu_semantics`
  remains skipped because CUDA is unavailable (pytest reports the location
  as `tests\test_gpu_visualization.py:61`).
- `python -m compileall -q tpcn tests`: passed.
- Pylance diagnostics on all four touched Python files: no errors. The three
  files `tpcn/temporal_scale.py`, `tests/test_luna12l_temporal_scale.py` and
  `tests/test_spiral_benchmark.py` report no diagnostics. In
  `tpcn/spiral_benchmark.py`, Pylance reports the pre-existing severity-4
  unused import `"Any"` on the unchanged `typing` import; that unrelated
  warning was not modified.
- `git diff --check`: passed.
- `git status --short artifacts/`: empty before and after implementation;
  frozen historical artifacts remain unchanged.
- The corrected Luna-12L handoff and the Luna-0 direction/decay review
  handoff have no worktree changes.

## Architecture and scientific-provenance audit

| Clause | Result |
|---|---|
| A01 | PASS — no timing or runtime architecture change. |
| A03 | PASS — routing behavior unchanged. |
| A04 | PASS — bounded historical topology/configuration preserved. |
| A06 | PASS — prediction semantics unchanged. |
| A07 | PASS — labels remain external to structural evidence. |
| A08 | PASS — deterministic and bounded execution preserved. |
| A10 | PASS — proxy energy remains diagnostic and uncalibrated. |
| A14 | PASS WITH HISTORICAL-COMPATIBILITY DISTINCTION — current ACP-0007 E2 structural semantics are unchanged. |
| A15 | PASS FOR SOFTWARE EXPERIMENT ONLY. |

```text
Architecture Contract: UNCHANGED
ACP-0007: UNCHANGED
ACP required: NO
architecture change: NO
core runtime change: NO
current E2 experiment: NOT PERFORMED
E2 pruning: NOT AUTHORIZED
N3: NOT AUTHORIZED

historical compatibility: ESTABLISHED
historical Luna-12L verdict: NOT SUPPORTED / UNCHANGED
current E2 four-class validation: NOT ESTABLISHED
task efficacy: NOT ESTABLISHED
resource benefit: NOT ESTABLISHED
hardware equivalence: NOT ESTABLISHED
```

**Luna-32: IMPLEMENTED / PUBLISHED / AWAITING INDEPENDENT REVIEW.** Required
next stage: Luna-0 independent review. Luna-32 does not self-close and does
not authorize Luna-33.
