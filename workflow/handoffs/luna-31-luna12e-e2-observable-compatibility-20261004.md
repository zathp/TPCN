# Luna-31 completion handoff — Luna-12E EXCURSION_V1 observable compatibility

```yaml
tpcn_handoff:
  agent: Luna-31
  luna_identifier: "Luna-31"
  descriptive_name: "Luna-12E EXCURSION_V1 Observable Compatibility Correction"
  task_id: "luna-31-luna12e-e2-observable-compatibility-20261004"
  component: "tests/test_luna12e_integration.py"
  status: "complete"
  contract_version: "1.2"
  branch: "main"
  base_revision: "2177038c73c6829d9d3577f0c5e452412940cbdd"
  result_revision: "see Revisions"
  classification: ["IMPLEMENTATION", "TEST COMPATIBILITY", "FOCUSED VERIFICATION"]
  architecture_change: false
  proposal: null
  files_changed:
    - tests/test_luna12e_integration.py
    - workflow/handoffs/luna-31-luna12e-e2-observable-compatibility-20261004.md
  terminal_verdict: "PASS — LUNA-31 LUNA-12E EXCURSION_V1 OBSERVABLE COMPATIBILITY CORRECTION READY FOR INDEPENDENT REVIEW"
```

Status: IMPLEMENTED / PUBLISHED / AWAITING INDEPENDENT REVIEW (not closed; no successor authorized).

## Revisions
- Authorization baseline: `8d5f7f5ad1c594df3cd886de327eb14c3dfbe15c`
- Authorization publication: `2177038c73c6829d9d3577f0c5e452412940cbdd`
- Execution starting revision: `2177038c73c6829d9d3577f0c5e452412940cbdd` (HEAD == origin/main, clean)
- Implementation / handoff revisions: the Git commit(s) containing this file; final origin/main reported on return.
- The opaque revision token in the source request does not resolve in Git (recorded by Luna-0); ancestry was verified against `8d5f7f5`/`2177038`.

## Environment
Tests run with Python 3.11.5 (`...\Python311\python.exe`); the shell `python` is 3.10.8 and was used only for `--version`.

## Changes (tests only)
1. Routed-topology test renamed `..._and_prediction_loss_changes` -> `test_experiment_readout_consumes_routed_activity_and_topology_changes_work` (stale invariant name; collection reconciled below). Configured `neuron_model="EXCURSION_V1"`.
   - Kept: no `neuron-0 -> neuron-1` trace without edge; trace present with edge; `event_count` increases.
   - Added: `edge_transfer_proxy` without edge == 0 and with edge greater; `maximum_route_depth` increases.
   - Removed: required prediction-loss inequality (stale oracle). Equal loss is permitted; only finiteness is asserted. Probe values: loss 1.1724999999999999 in both conditions; event count 12 -> 14; edge_transfer_proxy 0 -> 1.358357398350786; max route depth 0 -> 1.
2. Reset/identity test: identity stability kept; legacy `0.0`/`1.0` clock assertions replaced by terminal clock == last external timestamp (1.0) + `settling_horizon` (4.0) = 5.0 (observed 5.0 for both neurons), `mode == E1Mode.N`, `state == 0.0`, `pending_event is None`.
3. Added small `test_tanh_legacy_point_clocks_legacy_compatibility_only` (LEGACY COMPATIBILITY ONLY; clocks [0.0, 1.0]; not a gate).
4. The first three historical Luna-12E component tests are unchanged.

## Verification
- `python -m pytest -q tests/test_luna12e_integration.py`: 6 passed.
- EXCURSION_V1 integration/E2 (`test_excursion_integration`, `test_e2_multi_excursion`, `test_e2_ir2`, `test_luna28_excursion_structural_growth`) plus `test_predictive_coding.py` (multi-hop prediction-error routing coverage): 152 passed.
- Full suite `python -m pytest -q -rs`: 899 passed, 9 failed, 1 skipped (CUDA unavailable); 909 collected. Remaining failures are exactly the known out-of-scope groups: 8 in `tests/test_luna12l_temporal_scale.py` and 1 in `tests/test_spiral_benchmark.py`. Zero Luna-12E failures; no new regressions.
- Collection: 909 (baseline 908 + 1 new legacy test). Renamed test reconciled (old name -> new name); no deletion, xfail, skip or deselection.
- `python -m compileall -q tpcn tests`: exit 0. Diagnostics on the test file: no errors. `git diff --check`: clean (only CRLF autocrlf notice).
- No production file changed. Not run: Luna-12L/spiral repairs (out of scope).

## Architecture audit
A01 PASS; A02 PASS; A03 PASS; A04 PASS; A06 PASS (no loss delta required); A07 PASS; A08 PASS; A15 PASS FOR SOFTWARE REFERENCE ONLY.
Architecture Contract: UNCHANGED. ACP-0007: UNCHANGED. ACP required: NO. Architecture change: NO. Production semantic change: NO. E2 pruning: NOT AUTHORIZED. N3: NOT AUTHORIZED.

task efficacy: NOT ESTABLISHED
resource benefit: NOT ESTABLISHED
hardware equivalence: NOT ESTABLISHED

## Terminal verdict
PASS — LUNA-31 LUNA-12E EXCURSION_V1 OBSERVABLE COMPATIBILITY CORRECTION READY FOR INDEPENDENT REVIEW. Return to Luna-0 for independent review.
