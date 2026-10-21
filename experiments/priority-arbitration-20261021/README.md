# Priority arbitration experiments — 21 October 2026

The [oscillatory priority learning report](oscillatory-priority-test-v1/REPORT.md) records a completed synthetic comparison: the proposed error-amplitude/time-scaled oscillator learned, but failed the predeclared improvement criterion against paired perturbation and fixed-frequency controls. This is external training research, not a neural qualification or production integration.

## Archived packages

- [Local priority weighted lottery](local-priority-lottery-v1/README.md): bounded seeded reference arbiter, 15 unit tests, and illustrative untrained weights.
- [Arbiter evaluation](local-priority-lottery-tests-20261021/REPORT.md): sampling, replay, queue checks, and the strict-priority fairness limitation.
- [Oscillatory training comparison](oscillatory-priority-test-v1/REPORT.md): prospective plan, learner, 11 unit tests, 192 original runs, model snapshots, results, and three exact verification replays.

Each package retains its original manifest and artifact bytes. The arbiter package is a sibling dependency of the two study packages. Runtime imports do not depend on the original chat workspace. Historical output records may retain original paths.

## Verification

From this directory, with Python 3.11 and bytecode writes disabled:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest discover -s local-priority-lottery-v1 -p 'test_*.py'
python -m unittest discover -s oscillatory-priority-test-v1 -p 'test_*.py'
```

The study scripts create evidence files and should be run only in a fresh copy, preserving the archived results. No additional training run was used to revise the reported comparison during publication. The E1 rearm issue remains unresolved; these results do not clear R4 or Luna-72B.
