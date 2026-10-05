# Luna-0 Independent Post-Luna-41 Review — ACP-0008 Temporal Calibration

```yaml
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Independent post-Luna-41 scientific and governance review"
  task_id: "luna-0-independent-review-luna41-acp0008-temporal-calibration-20261005"
  component: "ACP-0008 bounded temporal calibration and ordinary-w=1 relay mechanism"
  status: "complete"
  contract_version: "1.0"
  branch: "main"
  base_revision: "e8639fc2563862b9d35bb7d9c951c59e137c12d0"
  result_revision: "commit containing this handoff"
  dependencies:
    - "Luna-41 execution: workflow/handoffs/luna-41-acp0008-temporal-calibration-20261005.md"
    - "Luna-0 calibration authorization: workflow/handoffs/luna-0-acp0008-calibration-decision-20261005.md"
    - "Accepted experimental ACP-0008"
    - "Independent post-Luna-40 and post-Luna-39 reviews"
  owner: "Project owner"
  classification:
    - "independent scientific and governance review"
    - "Luna-41 bounded execution and Phase-B gate pass; provenance caveat"
    - "scientific verdict blocked at Phase-A normalized-input gate"
    - "no production or architecture change"
  verdict: "BLOCKED; no valid calibrated candidate or Phase-B result"
  hypothesis: "Task-independent temporal calibration enables a bounded integration-mediated relay emission under ordinary fixed-w=1 routed input."
  conclusion: "The 0.0125 near-triple trace emits in the normalized test setup, but the repeated source transfers exceed the declared 0.4 payload. No candidate validly passes Phase A; multi-hop onward routing is untested."
  architecture_change: false
  acp_change: false
  follow_up_authorized: false
  luna42_created: false
  acp0008_status: "experimental, opt-in, unpromoted"
  tests_passing:
    - "Luna-41 focused tests: 6 passed."
    - "Full repository suite: 1015 passed, 1 skipped; 1016 collected."
    - "Independent Phase-A rerun: two runs matched each other and the retained digest."
    - "Independent ACP-0008 recurrence reconstruction: 68 trace steps, maximum state-equation absolute discrepancy 1.271e-21."
    - "git diff --check."
  tests_failed: []
  tests_not_run:
    - "Phase B was correctly gated off because Phase A selected no valid candidate."
    - "Phase-B replay and multi-hop relay-to-destination route audit are not applicable; no such events were generated."
    - "Hardware equivalence, task efficacy, structural growth, and ACP-0008 promotion were not authorized."
  files_changed:
    - "workflow/handoffs/luna-0-independent-review-luna41-acp0008-temporal-calibration-20261005.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  recommended_next_agent:
    - "Project owner to decide how to resolve the source-amplitude/normalized-fixture mismatch before any further calibration or mechanism experiment."
```

## Reviewed revision and procedure

Fetched `origin/main` and verified the exact Luna-41 ending revision before
review:

- `HEAD == origin/main == e8639fc2563862b9d35bb7d9c951c59e137c12d0`
- branch `main`
- clean worktree and index.

Reviewed the Luna-41 contract, execution handoff, all four calibration
artifacts, runner and tests; ACP-0008 and its production implementation;
the Luna-0 authorization; independent post-Luna-40 and post-Luna-39 reviews;
Luna-40 artifacts; current workflow and changelog. The implementation
reviewed is the committed Luna-41 runner at the ending revision. Its retained
`execution_revision` field is `null`; the commit contains the runner and its
evidence together, and an independent replay from that committed runner
reproduced the retained digest. The execution revision omission is recorded
as a provenance limitation, not evidence of parameter retuning.

The Luna-41 execution commit changes exactly its owned runner, focused tests,
four artifacts, and execution handoff. No production module, ACP, architecture
contract, shared governance document, WEMA, optimizer, or Luna-42 authorization
was included. The separate source inspection confirmed that only
`decay_rate_z` varies across enabled calibration arms; other ACP-0008
parameters remain fixed and the disabled control uses the production
`integration=None` path.

## Independent Phase-A reconstruction

The frozen configuration is exactly the four-candidate set
`0.1, 0.05, 0.025, 0.0125`. Every enabled arm uses
`theta_E=1`, `theta_Z=1`, `input_gain=1`, `z_max=4`, fast decay `1`,
and ACP-0007 disabled. The Phase-A edge is ordinary Model-B
`source -> relay`, `w=1`, delay `1`. Inputs are generated through the
production source, event queue and bounded topology, not hand-authored routed
events.

For each candidate, I reconstructed all six declared fixtures. Table values
are the absolute relay `z` after the last nonzero input, before any
post-discharge reduction; `emissions` counts relay canonical emissions.

| `decay_rate_z` | Isolated `z` / emissions | Near-pair `z` / emissions | Near-triple `z` / emissions | Far-triple `z` / emissions | Negative near-triple | Disabled near-triple |
|---:|---:|---:|---:|---:|---|---|
| 0.1 | 0.400000 / 0 | 0.510109 / 0 | 0.540419 / 0 | 0.402310 / 0 | No emission; sign preserved; payload gate fails | No emission; production integration disabled; payload gate fails |
| 0.05 | 0.400000 / 0 | 0.609866 / 0 | 0.719975 / 0 | 0.432606 / 0 | No emission; sign preserved; payload gate fails | No emission; production integration disabled; payload gate fails |
| 0.025 | 0.400000 / 0 | 0.689735 / 0 | 0.899601 / 0 | 0.540418 / 0 | No emission; sign preserved; payload gate fails | No emission; production integration disabled; payload gate fails |
| 0.0125 | 0.400000 / 0 | 0.740433 / 0 | 1.030168 / 1 | 0.719973 / 0 | One negative integrated emission; sign preserved; payload gate fails | No emission; production integration disabled; payload gate fails |

The isolated and far fixtures pass the route-payload criterion for every
candidate. For the repeated near fixtures, the first routed contribution is
exactly `+/-0.4`; subsequent positive payloads are
`0.4000008889685561` and `0.4000008889707768`, with exact sign-mirrored
negative values. The maximum absolute error is `8.889707767689714e-7`.
The same repeated-source discrepancy occurs in the integration-disabled
control, demonstrating that it originates in source state, not relay
integration.

The source's fast state is not fully zero after each ordinary excursion.
Consequently later canonical source payloads are
`0.42364998848995` and `0.423649988492594`, instead of
`atanh(0.4)=0.42364893019360184`; the unchanged `tanh(w * payload)` route at
`w=1` produces the observed payloads above. Far-spaced inputs allow enough
fast-state decay that each routed transfer returns to `0.4`.

The pre-execution analytic oracle used ideal `+/-0.4` routed inputs. The
observed final near-pair, near-triple pre-discharge, and far-triple `|z|`
values differ from its predictions by at most `1.645553490581264e-6`, within
the declared analytic tolerance `1e-5`. Only `decay_rate_z=0.0125` crosses
the near-triple discharge boundary in the enabled arms. Thus the predicted
*threshold-crossing pattern* is partly confirmed, but this does not pass the
full fixture: the actual near-route inputs violate the contract's normalized
payload precondition.

## Equation and mechanism audit

Independently replayed the ACP-0008 equation over all **68** retained
integration trace entries across all enabled records. For each event the
reconstruction starts from prior `z`, applies
`z_decayed = z_prior * exp(-decay_rate_z * dt)`, adds the signed contribution
only when the production trace says integration is active, clips to
`[-z_max, z_max]`, applies the signed one-quantum discharge condition, and
compares post-discharge state to the trace.

Maximum absolute differences across all records were:

| Trace quantity | Maximum absolute discrepancy |
|---|---:|
| `z_after_decay` | `1.271e-21` |
| `z_after_input` | `1.271e-21` |
| `discharge_amount` | `0` |
| `z_post_discharge` | `1.271e-21` |

The positive and negative `0.0125` near triples each record one
`integrated_discharge`, not a direct emission, with canonical payloads
`+0.350000472048906` and `-0.350000472048906`. Ordinary emission-amplitude
and causality checks reconcile. No candidate emits on an isolated input,
near pair, far triple, or disabled control. Negative evidence remains
negative throughout route, integration, discharge, and output.

The disabled control constructs the relay with `integration=None`; its
`integration_state` is absent (`null`) and it records no integration trace.
No hidden slow state is retained by that arm.

All enabled neutral probes occur after at least `10 * tau_z`. The maximum
observed `|z|` after a neutral probe is `4.084181869340788e-5`, below the
`1e-4` bound. No relay canonical emission timestamp is at or after a probe
timestamp. One record-field caveat: `emission_count_after_probe` is populated
from the cumulative relay-emission list, rather than filtering by probe
timestamp. I used retained canonical-emission timestamps to verify the
no-spontaneous-emission condition independently.

Bound/resource checks pass. Across Phase-A records, maxima are 15 processed
events (limit 64), queue peak 4 (capacity 64), 9 source events (budget 64),
and 6 relay events (budget 64). State bounds hold; internal emissions use the
existing positive-delay production path, with no zero-time loop or event
explosion.

## Selection, freeze, replay, and Phase-B gate

The declared selection rule is the largest `decay_rate_z` whose **every**
Phase-A fixture passes. Reapplying it to the per-fixture records selects no
candidate; the retained selected value is `null`. The `0.0125` candidate
would meet the emission-count/sign pattern if the source-payload check were
ignored, but ignoring that explicit prerequisite would be post-hoc criterion
relaxation and is not accepted.

The freeze records the null selection before any Phase-B stream creation.
Independent checks confirmed the frozen configuration digest, freeze-record
digest, Phase-A digest and result digest. The candidate selection is based
solely on Phase-A; the Phase-B code is reached only in the non-null selection
branch, after the freeze write. No Phase-B routine was called or stream
consumed. The contract-required stop was therefore obeyed.

I reran the complete Phase-A design twice from reset using the committed
runner. Both independent aggregate digests matched each other and the retained
digest:

`fcbea9694a19ce407544c6394cb51432a64ff59d39437e834abc193aff4f9cd2`

This covers candidates, fixture outcomes, state traces, emission identities,
and routed arrivals. Phase-B replay is not run because Phase B is correctly
gated off. Phase A uses only the single `source -> relay` edge; it does not
include a destination or establish onward multi-hop routing.

## Verdict and architectural interpretation

**Bounded-execution and Phase-B-gate compliance: PASS WITH PROVENANCE
CAVEAT. Scientific verdict: BLOCKED at the Phase-A normalized-routed-payload
gate.** Luna-41 executed the frozen Phase-A matrix, retained the failures,
performed its required replay, selected no candidate, and correctly did not
start Phase B. It did not tune or expand the experiment. One handoff
requirement is incomplete: `results.json` has `execution_revision: null`.
The enclosing commit binds the runner and artifacts together, and an
independent replay from that committed source reproduced the artifact digest;
however, the result itself does not explicitly record its source revision.

The contract explicitly requires stopping before Phase B if repeated source
events fail to produce the declared routed payload. The result is not a valid
negative calibration finding under exact normalized repeated inputs, nor a
valid calibration success. The observed `0.0125` relay emission is useful
mechanistic evidence, but it cannot replace the failed fixture precondition.
The contract supplies no explicit route-payload tolerance; the runner used
`1e-12`, and the observed dynamics deviation is about `8.9e-7`. This review
does not widen that tolerance or amend the experiment.

**Can task-independent temporal requirements calibrate ACP-0008 so ordinary
fixed-`w=1` routed input produces bounded integration-mediated relay
emission?** Not established by this run. The normalized near-triple fixture
produced one signed integration-mediated relay spike at the slowest candidate,
with bounded/leaky state and a recurrence matching ACP-0008, but the source
did not deliver the exact predeclared `0.4` repeated contributions. Phase B
was not reached.

**Does that relay emission produce valid multi-hop onward routing through
the existing topology?** Not established. Phase A has no onward edge, and
Phase B was not run. No `relay -> destination` event may be inferred from
the Phase-A relay spike.

Luna-40 remains historically **NOT SUPPORTED IN THIS SETUP** under the prior
ACP-0008 default and its tested growth conditions; this review does not
contradict or revise that result. The evidence does not support ACP-0008
promotion. Its status remains **experimental / opt-in / unpromoted**.

No Luna-42 was created or authorized. The proposed candidate-opportunity
diagnostic depends on a valid frozen calibration and demonstrated ordinary
multi-hop relay route, neither of which is available here. Do not retune
decay rates, adjust route tolerance, change the source fixture, implement
WEMA, or begin ACP-0007 growth work without a separate project-owner
decision. Return the amplitude/precondition mismatch and the tolerance
ambiguity to the project owner.

## Validation

- Luna-41 focused tests: **6 passed**.
- Full repository suite: **1015 passed, 1 skipped; 1016 collected**.
- Skip reason: CUDA unavailable (`tests/test_gpu_visualization.py:61`).
- Independent Phase-A replay: two fresh runs matched each other and retained
  digest.
- Analytic prediction: **partly confirmed**; only `0.0125` crossed/emitted
  as predicted, numerical `z` remained within oracle tolerance, but the
  repeated route payload precondition failed.
- Independent ACP-0008 recurrence reconstruction: **68 entries**, maximum
  absolute discrepancy `1.271e-21`.
- `git diff --check`: passed.

No independent Phase-B run was performed; Phase B is not applicable after
the valid Phase-A gate failure.

Commands/procedures:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_luna41_acp0008_temporal_calibration.py -q
.\.venv\Scripts\python.exe -m pytest -q -rs
git diff --check
```

The independent replay invoked `_run_phase_a_once()` twice from the committed
runner and recomputed each canonical digest; the recurrence audit separately
recomputed decay, signed input contribution, discharge, and post-discharge
state from the retained event traces.
