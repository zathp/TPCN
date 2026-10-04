# Luna-0 Independent Review — Luna-32 Historical Luna-12L / Spiral Model-Explicit Compatibility

```yaml
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  task_id: "luna-0-independent-review-luna-32-historical-temporal-spiral-model-compatibility-20261004"
  contract_version: "1.2"
  status: "complete-pass-closed"
  branch: "main"
  review_starting_revision: "030a1e72578bb78cd45b67a90e97b93987259d72"
  authorization_source_revision: "392ce2510660221d7486a59f184a1eeba6f17634"
  authorization_publication_revision: "5696b2ff0886d589559b366e885661e5106be1dd"
  implementation_revision: "a70c8cd6df7cdbb98ef11e7a76711e5ead918cb8"
  handoff_publication_revision: "030a1e72578bb78cd45b67a90e97b93987259d72"
  architecture_change: false
  proposal: null
  terminal_verdict: "PASS — LUNA-32 HISTORICAL LUNA-12L / SPIRAL MODEL-EXPLICIT COMPATIBILITY INDEPENDENTLY VERIFIED / CLOSED"
  successor: "NOT AUTHORIZED"
```

## Review baseline and lineage

Review began at clean synchronized `main`, with `HEAD == origin/main ==
030a1e72578bb78cd45b67a90e97b93987259d72`, subject
`docs: publish Luna-32 compatibility handoff`. The commit lineage is:

```text
392ce2510660221d7486a59f184a1eeba6f17634  Luna-31 independent closure
5696b2ff0886d589559b366e885661e5106be1dd  Luna-32 authorization publication
a70c8cd6df7cdbb98ef11e7a76711e5ead918cb8  Luna-32 implementation
030a1e72578bb78cd45b67a90e97b93987259d72  Luna-32 completion-handoff publication
```

The Luna-32 implementation delta changes exactly:

- `tpcn/temporal_scale.py`
- `tpcn/spiral_benchmark.py`
- `tests/test_luna12l_temporal_scale.py`
- `tests/test_spiral_benchmark.py`

The Luna-32 handoff publication adds only
`workflow/handoffs/luna-32-historical-temporal-spiral-model-compatibility-20261004.md`.
There are no changes to artifacts, ACP-0007, the Architecture Contract,
core-runtime files, run scripts, frozen historical handoffs, or unrelated
tests. The handoff publication and implementation commits include the required
Copilot co-author trailer.

## Historical scientific evidence

The corrected historical Luna-12L verdict remains **NOT SUPPORTED** and
unchanged: four-class/scale benefit was not demonstrated; the reference-scale
policy distinction did not survive expanded scale; temporal proxy energy was
higher than fixed; and the learned-edge intervention changed routed
computation. Shortcut formation itself was not refuted.

The required not-same-experiment disclosure is present. The preserved
authorization comparison records event counts 30/30 and classifier topology
edge counts 30/30 matching the artifact, but proxy energy 0/30, replay digests
0/30, and accuracy 23/30. The Luna-32 handoff explicitly says its current
compatibility run is **NOT THE SAME EXPERIMENT AS THE RETAINED LUNA-12L
ARTIFACT** and is not a reproduction, correction, superseding result or new
efficacy evidence.

No file under `artifacts/` or either named historical handoff changed between
the authorization and review revisions. `artifacts/temporal-scale-12l` has
the same Git tree object at both revisions:
`063705fa31d3d67e4ebddd29a4ae4968e25edd02`. The working tree is also clean
for artifacts. Historical result integrity: **UNCHANGED**.

## Five-policy classifier audit

The actual `ExperimentConfig` captured at `run_policy_control()` confirms
`neuron_model="TANH_LEGACY"` for both normal and reverse-order classifier
calls at each scale and policy. `structural_policy` is the original requested
policy; plasticity is disabled only for `fixed`. No translation table or
`e2_local_temporal` alias exists. Current `ExperimentConfig` default remains
`EXCURSION_V1`.

| Scale | Policy | Independent config digest prefix | Classifier topology edges |
|---|---|---|---:|
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

These runtime results confirm `fixed` and `temporal` classifier topology state
differs; identical edge counts among growth policies do not imply identical
policy semantics. The checked historical scales remain exactly:

- Reference: 7 nodes, edge capacity 6, fan-in/out 2, candidate/history 8,
  queue/event 16, growth attempts 3.
- Expanded: 12 nodes, edge capacity 10, fan-in/out 3, candidate/history 12,
  queue/event 24, growth attempts 5.

Each result preserved requested and executed scale identity. Reference and
expanded classifier configs/digests differ.

### Actual execution and provenance

The unchanged `run_policy_control()` validates the historical policy set and
passes the supplied config to `_control()`. The inspected
`ExperimentRunner._adapt_topology()` contains the TANH legacy adaptation:
`reversed` selects the preceding node, `temporal` selects index + 2, `random`
uses a seeded destination, and `baseline` takes the next node; fixed does not
adapt. All four growth policies have `structural_plasticity=True` and flow
through that legacy branch. Thus requested/executed policy equality is backed
by actual configured execution, not only an echoed string.

The deliberate mismatch test independently raises the intended
`RuntimeError: classifier condition provenance does not match requested
condition`, after a valid TANH legacy classifier run. It does not fail first
at E2 configuration validation.

The two-system provenance remains honest: `run_luna12l_condition()` pairs
`run_temporal_capacity(policy, ...)` metrics with an `ExperimentRunner`
classifier condition using the same policy name. These remain separate
implementations. Neither `run_temporal_capacity()` nor its implementation
was changed or claimed to be identical to classifier adaptation.

### Luna-12L test-strength and label isolation

The before/after test diff removes or weakens no existing assertions for
retained policy/scale rows, shortcut selection, causal intervention,
requested/executed provenance, policy-dependent topology, scale provenance,
serialization or deliberate mismatch. The added assertions capture the
actual two classifier configs and verify model, policy and plasticity flags.

`test_labels_do_not_change_canonical_four_class_trace` is unchanged in
scientific meaning and continues to exercise the current default canonical
path; it is not mislabeled as a historical classifier-policy comparison.

## Spiral matched-model audit

`run_controls()` sets `neuron_model="TANH_LEGACY"` in its shared `base` before
constructing every control. The independent bounded fixture captured all ten
configs; all ten, including both fixed/no-learning controls, use the same
legacy model. The exact control-name set is unchanged. Two independent
`run_controls()` invocations compare equal (`first == second`); the structural
control recorded `mutation_count == 1`. That mutation is historical TANH
compatibility behavior only and does not authorize E2 pruning.

The structural control is not the only TANH control; no cross-model
comparison exists. `run_policy_control()` was not forced to TANH, its policy
set was not expanded, and it contains no legacy-to-E2 policy translation.

## Current E2 and architecture protections

`ExperimentConfig().neuron_model` independently evaluates to
`EXCURSION_V1`. Existing regression tests continue to enforce the E2 growth
configuration: observation enabled, plasticity enabled, `e2_local_temporal`,
explicit local neighbors, and declared bounded parameters. No E2 pruning
semantics were changed or authorized.

Architecture state: Contract **1.2 / unchanged**; ACP-0007 **ACCEPTED /
unchanged**; Luna-28 through Luna-31 **CLOSED / independently verified**;
E2 pruning **NOT AUTHORIZED**; N3 **NOT AUTHORIZED**.

| Clause | Independent disposition |
|---|---|
| A01 | PASS — no runtime or timing architecture change. |
| A03 | PASS — routing semantics unchanged. |
| A04 | PASS — historical finite topology/configuration bounds preserved. |
| A06 | PASS — prediction semantics unchanged. |
| A07 | PASS — external labels remain outside structural evidence. |
| A08 | PASS — determinism and bounded execution preserved. |
| A10 | PASS — proxy energy remains diagnostic and uncalibrated. |
| A14 | PASS WITH HISTORICAL-COMPATIBILITY DISTINCTION — current ACP-0007 E2 semantics unchanged. |
| A15 | PASS FOR SOFTWARE EXPERIMENT ONLY — no hardware equivalence claim. |

## Independent validation

- Focused Luna-12L and spiral tests: **18 passed**.
- Legacy/E2 regression selection
  (`test_experiments.py`, `test_structural_plasticity.py`, `test_topology.py`,
  `test_luna28_excursion_structural_growth.py`, `test_luna12b_integration.py`):
  **96 passed**.
- Full suite: **908 passed, 0 failed, 1 skipped**.
- Collection audit: **909 tests collected**. The tests remain present; no
  delete, rename-to-evade, xfail, unconditional skip or deselection was
  introduced in the Luna-32 delta.
- The sole skip is the unchanged
  `tests/test_gpu_visualization.py::test_cuda_records_have_cpu_semantics`,
  because CUDA is unavailable.
- `python -m compileall -q tpcn tests`: passed.
- Pylance diagnostics: zero errors. `temporal_scale.py` and both touched test
  files have no diagnostics. The only diagnostic is the severity-4 unused
  `Any` import in `spiral_benchmark.py`; the import predates Luna-32 and is
  unchanged in its implementation diff, so it is not a Luna-32 regression.
- `git diff --check`: passed.

## Closure decision

```text
historical Luna-12L / spiral compatibility: ESTABLISHED / CLOSED / VERIFIED
historical model: TANH_LEGACY made explicit
historical Luna-12L verdict: NOT SUPPORTED / UNCHANGED
current EXCURSION_V1 default: UNCHANGED
ACP-0007: UNCHANGED
new E2 four-class experiment: NOT PERFORMED
current E2 four-class validation: NOT ESTABLISHED
ACP-0007 four-class efficacy: NOT ESTABLISHED
task efficacy: NOT ESTABLISHED
resource benefit: NOT ESTABLISHED
hardware equivalence: NOT ESTABLISHED
E2 pruning: NOT AUTHORIZED
N3: NOT AUTHORIZED
successor: NOT AUTHORIZED
```

**PASS — LUNA-32 HISTORICAL LUNA-12L / SPIRAL MODEL-EXPLICIT COMPATIBILITY
INDEPENDENTLY VERIFIED / CLOSED** within the historical code-path
compatibility scope only. Luna-33 is **NOT AUTHORIZED**.
