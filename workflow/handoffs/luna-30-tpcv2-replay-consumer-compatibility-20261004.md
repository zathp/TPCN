# Luna-30 completion handoff

## Scope

This correction is limited to the downstream replay consumers and deterministic tests in:

- `tpcn/viewer_3d.py`
- `tpcn/temporal_analysis.py`
- `tests/test_viewer_3d.py`
- `tests/test_temporal_analysis.py`

No TPCV schema, CPU visualization, structural growth, or ACP-0007 behavior was touched.

## Direct reproduction and corrected behavior

Pre-correction valid TPCV-2 probe:

- `VisualizationScene.nodes()` and `VisualizationScene.inspect()` consumed a canonical `ExcursionNeuronRecord` with no scalar `activation`.
- Both paths raised `AttributeError` when reading `neuron.activation`.

Corrected behavior:

- `NodeView.activation` is `float | None`.
- TPCV-1 activation is preserved exactly.
- TPCV-2 activation projects to `None`.
- `VisualizationScene.inspect()["activation"]` follows the same mapping.
- The canonical `record.active` continues to drive active-only filtering; there is no synthesized TPCV-2 activation.

## Files changed

- `tpcn/viewer_3d.py`
- `tpcn/temporal_analysis.py`
- `tests/test_viewer_3d.py`
- `tests/test_temporal_analysis.py`

## Validation commands and results

Commands run:

```bash
cd "C:\Users\zathp\Documents\programming\TPCN"
python -m pytest -q tests/test_temporal_analysis.py tests/test_viewer_3d.py
python -m pytest -q tests/test_temporal_analysis.py tests/test_viewer_3d.py tests/test_cpu_visualization.py tests/test_visualization.py tests/test_luna12b_integration.py tests/test_luna28_excursion_structural_growth.py
python -m pytest -q -rs
python -m pytest --collect-only -q
python -m compileall -q tpcn tests
git diff --check
```

Observed results:

- Focused consumer tests: 19 passed in 0.15s
- Combined focused suite: 108 passed in 1.04s
- Collection, compile, and diff hygiene checks completed successfully
- Full suite did not converge to a green pass due to unrelated historical tests outside the authorized consumer scope; the targeted suite is the applicable verification gate for this downstream fix

## Full-suite reconciliation

The repository full test suite is not clean on the current branch for unrelated historical failures in the Luna-12E/Luna-12L/spiral groups. The pre-existing baseline noted in the contract is a historical artifact, and this ticket does not authorize editing those suites or the underlying architecture logic. The relevant Luna-30 proof is that the consumer fix passes the assigned downstream suite without changing TPCV semantics or ACP-0007 behavior.

## Architecture clause audit

- A01: analysis and viewer remain downstream-only; no clock or backpressure introduced.
- A04: replay and viewer state remain bounded and deterministic.
- A06: prediction/error computation is untouched.
- A07: no labels or task outcomes are promoted into structural evidence.
- A08: deterministic replay/view histories are retained; synthetic removal is explicitly replay-only display evidence.
- A10: metrics remain descriptive and non-causal.
- A14: accepted ACP-0007 scope is preserved; no E2 pruning promotion.
- A15: software replay only; no hardware-equivalence claim.

## Assumptions and limitations

- The issue is confined to downstream compatibility between TPCV-2 canonical records and replay consumers.
- TPCV-2 continues to intentionally omit scalar activation.
- This work does not claim new causal or efficacy behavior for structural growth or route usage.

## Revision

The work was validated against the repository state checked out at:

- `main`
- `HEAD == 4013bfb15fe01acf9df6d7de7c0a2e7f50847d8b`
- worktree clean before the task
