# Luna-63A: isolated binary adaptive decay

ISOLATED EXPERIMENTAL MODEL, opt-in and never imported by production.
Question: **can the state wait?** One bounded signed scalar uses prior-gate
analytic decay `z *= exp(-dt/8)` in NORMAL and exact identity in HOLD.
Only fresh initialization preloads state. Cues accept integer R=0 or R=1,
never a scalar value, symbol, answer or output request. Settlement precedes
gate change. No output API, fast state, threshold, discharge, learning,
predictor, routing or network exists.

Frozen contract: `.github/agents/luna-63a.agent.md`, committed at governance
baseline `e52098b2141a3f121f23b512e877783a64ef8baa`, blob
`a54ca6f22ff6b75e4b0297dac8012db4354df656`.
Scientific source baseline `8123147e04c6044d12023f541cf63130cdbb7dcc`.
`protocol.json` freezes all eleven schedules and three rational/float
preloads, exact insertion ties, TTL, bounds and acceptance criteria.
One due expiry at 64 is drained after each schedule unless the boundary
handler already canceled it. Expiry records the stored value immediately
before direct invalidation; it does not evolve normally at/after 64.
At 65 only the terminal status is reported. No ID reuse or reset API exists.

The focused test has an independent 60-digit Decimal exponential oracle
based on total time in R=1, not model functions. It measures only after
materialization; expected values never enter computation. All valid rows
retain oracle, residual, tolerance and exact status/gate/tie checks.
Exact HOLD checks binary64 bits. Validation-only bounds/invalid-input
fixtures are not additional scientific arms. Same-platform replay repeats
all 33 instances freshly; JSON bytes must match. No cross-platform libm
identity is presumed.

## Reproduce after the pre-outcome commit is pushed

From the assigned isolated worktree, using Python 3.11+ and pytest:

```text
python -m pytest -q tests/test_luna63a_adaptive_decay.py
```

The artifact command is:

```text
python tests/test_luna63a_adaptive_decay.py --record PRE_OUTCOME_SHA
```

It writes only results/replay/manifest under `artifacts/luna63a`.
Outcome JSON contains no run/provenance labels. Manifest stores provenance
separately and records both artifact hashes. Manifest's own hash is recorded
externally in the handoff/publication to avoid recursive self-hashing.
Git blobs and checkout bytes are recorded separately without normalization.

Required unchanged regressions:
`test_event_runtime.py`, `test_excursion_neuron.py`,
`test_e2_multi_excursion.py`, `test_luna38_excursion_integration_state.py`,
`test_predictive_coding.py`, `test_luna47a_retention.py`,
`test_luna47d_output_model.py` under `tests/`. Full suite not required;
no production edits allowed. Historical failures must remain failures.

## Explicit departures and nonclaims

ACP-0008 requires strictly positive fixed effective decay; this isolated
component uses exact zero leak and a mutable local binary gate, plus a new
absolute wrapper TTL. No frozen production config is mutated or bypassed.
A01-A05/A07/A08 are preserved within component scope; predictive, energy
and credit capabilities A06/A09-A11 are absent from this assay, not removed
from TPCN. A12/A13 remain optional; A14 out of scope. A15 gate/register/
expiry mapping is qualitative only: no physical infinite retention claim.

Even support establishes no connected canonical neuron recall or emission,
sequence memory, task efficacy, hardware equivalence, ACP acceptance, core
promotion, integrated echo, Luna-64 or interlane composition. Independent
Luna-0 review remains mandatory. Original blocked handoff history is retained.
