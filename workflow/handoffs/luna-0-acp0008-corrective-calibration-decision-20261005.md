---
tpcn_handoff:
  agent: "Luna-0 Architecture Guardian"
  luna_identifier: "Luna-0"
  descriptive_name: "Corrective ACP-0008 calibration decision"
  task_id: "luna-0-acp0008-corrective-calibration-decision-20261005"
  component: "Production-derived normalized stimulus and provenance correction for ACP-0008 calibration"
  status: "complete"
  contract_version: "1.0"
  branch: "main"
  base_revision: "0ebb59c4fa61c5f2aad6ffa09341de1b342745bf"
  result_revision: "the commit that publishes this handoff"
  dependencies:
    - "Luna-41 execution and independent review"
    - "Accepted experimental ACP-0008"
    - "Project-owner direction supplied 2026-10-05"
  owner: "Project owner"
  classification:
    - "governance-only corrective decision"
    - "CALIBRATION RESULT UNRESOLVED DUE TO FIXTURE SPECIFICATION / PROVENANCE DEFECT"
    - "Luna-41 remains BLOCKED"
    - "Luna-42 AUTHORIZED / NOT EXECUTED"
    - "no architecture or production change"
  hypothesis: "A production-derived source fixture can define normalized fixed-w=1 routed inputs unambiguously and correct the Luna-41 fixture/provenance blocker without changing ACP-0008 or routing architecture."
  counter_hypothesis: "The causal source stimulus fails to produce stable, bounded, correctly routed events, or no frozen decay candidate meets the same task-independent temporal criteria."
  interfaces_relied_on:
    - "MultiExcursionNeuron and ordinary source canonical emission"
    - "BoundedTopology Model-B transform and EventQueue propagation"
    - "ACP-0008 IntegrationConfig"
  authorized_scope:
    - "Correct the calibration stimulus/provenance contract only."
    - "Replicate the four-candidate Luna-41 Phase A with the same selection rule and timing."
    - "Run Phase B only after valid Phase-A selection and immutable freeze."
  unauthorized_scope:
    - "No production equation, neuron, routing, topology, ACP, or Architecture Contract change."
    - "No candidate-grid expansion, threshold/time change, optimizer, task fitting, WEMA implementation, efficacy, growth, or promotion."
  controls:
    - "Isolated, near-pair, near-triple, far-triple, negative near-triple, and integration-disabled fixtures."
    - "If Phase A passes: calibrated, default, and disabled relay-stream arms."
  numerical_policy:
    exact:
      - "candidate and selection identities"
      - "event counts/identity/order and one-to-one source-emission/route/reception reconciliation"
      - "emission count and direct/integrated/none classification"
      - "fixture schedules, route paths, control enablement, replay digests"
      - "routed event payload identity between production queue and relay receipt"
    floating:
      - "tol(a,b) = 64 * sys.float_info.epsilon * max(1.0, abs(a), abs(b))"
      - "used only for independent source/Model-B/neuron equation comparisons, analytic recurrence, and bounded floating state checks"
      - "defined before execution from binary64 operation-rounding budget; not fitted to Luna-41 observations"
  architecture_invariants_touched:
    - "A01"
    - "A02"
    - "A03"
    - "A08"
    - "A15"
  preserves:
    - "Luna-41 BLOCKED verdict and historical evidence"
    - "ACP-0008 experimental, opt-in, unpromoted status"
    - "ACP-0007 unchanged and disabled"
    - "all prior Luna verdicts"
  architecture_change: false
  acp_change: false
  production_change: false
  wema: "Unresolved alternative architecture idea only; no implementation or experiment authorized."
  luna42_status: "AUTHORIZED / NOT EXECUTED"
  tests_passing: []
  tests_failed: []
  tests_not_run:
    - "Full test suite not rerun: governance and experiment-contract documents only; no production or executable code changed."
    - "Luna-42 is not executed in this decision pass."
  files_changed:
    - ".github/agents/luna-42.agent.md"
    - "workflow/handoffs/luna-0-acp0008-corrective-calibration-decision-20261005.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  unresolved:
    - "Whether any frozen candidate passes the corrected production-derived Phase-A fixtures."
    - "Whether the frozen candidate produces ordinary fixed-w=1 relay emissions and onward transfers in Phase B."
  recommended_next_agent:
    - "Luna-42 to implement and execute the authorized corrective replication from this published decision revision."
    - "Luna-0 for independent review after Luna-42 completes."
---

# Luna-0 decision — corrective ACP-0008 calibration

## Decision

**CALIBRATION RESULT UNRESOLVED DUE TO FIXTURE SPECIFICATION / PROVENANCE
DEFECT. Luna-41 remains BLOCKED. This is not evidence that ACP-0008 temporal
integration failed. Luna-42 is AUTHORIZED / NOT EXECUTED.**

This decision begins from the exact requested baseline:
`HEAD == origin/main == 0ebb59c4fa61c5f2aad6ffa09341de1b342745bf`, branch
`main`, clean index and worktree.

The existing production interfaces can express a causal source fixture
without changing architecture: submit a fixed external stimulus to an
ordinary source neuron, observe its canonical emission, route it through the
existing bounded Model-B edge, and deliver the actual queued payload to the
relay. Therefore the owner-directed condition for one narrow corrective
successor is satisfied.

## Luna-41 disposition

Luna-41 tested exactly `0.1`, `0.05`, `0.025`, and `0.0125`, with all other
ACP-0008 parameters fixed and ACP-0007 disabled. Its repeated near-spaced
source stimuli deterministically routed payloads
`0.4000008889685561` and `0.4000008889707768`, rather than the contract's
literal `0.4`; the contract had not defined an equivalence tolerance for
that mismatch. The runner's `1e-12` acceptance tolerance was undocumented
by the experiment contract. No candidate validly passed the literal
Phase-A gate, so Phase B correctly did not run. Keep this result **BLOCKED**; do not relabel
it **NOT SUPPORTED**.

The mechanics themselves were independently reproduced: only `0.0125`
crossed the near-triple discharge boundary; positive and negative integrated
emissions were symmetric; isolated/far/disabled controls remained silent;
68 production trace steps matched the ACP-0008 recurrence within
`1.271e-21`; neutral return, bounds and deterministic replay passed. Thus
the prior analytic threshold-crossing prediction is **partly confirmed** as
a mechanical prediction, but it is not a valid calibration result because
the declared exact input fixture was not delivered.

The prior review also recorded `results.json.execution_revision == null`.
Although the committed runner reproduced its Phase-A digest, that is a
provenance deficiency for a scientific claim and must be closed in Luna-42.
No Phase-B outcome exists, and no multi-hop relay-to-destination conclusion
may be drawn.

## Authorized corrective scope

Luna-42 is a corrective replication of Luna-41 Phase A and its gated Phase B,
not a new search. It may change only the source-stimulus specification,
production-derived payload/oracle provenance, explicit numerical comparison
rules, and execution/artifact provenance.

Keep exactly the four candidate values, the same fastest-decay-passing
selection rule, all ACP-0008 parameters other than the candidate, the same
near/far input times, thresholds, queue/event/topology bounds, and all
conceptual controls. Keep ACP-0007 disabled. Do not edit production code,
ACP-0008 equations, the Architecture Contract, or historical Luna-41
evidence.

The fixed source fixture is a default ordinary `MultiExcursionNeuron` with
fast decay `1`, `theta_E=1`, event budget `64`, and integration disabled.
Its external input is the predeclared binary64 value `1.6945957207744073`
(or its negative mirror), at the original fixture times: isolated `0`;
near pair `0, 12.9`; near triple `0, 12.9, 25.8`; far triple
`0, 51.6, 103.2`; negative near triple `0, 12.9, 25.8`; and disabled
near triple `0, 12.9, 25.8`.

The nominal `0.4` is only a normalization anchor for the isolated source
response. It must not be an injected relay payload or an exact repeated
route requirement. Use each actual Model-B payload emitted by the source
and routed by the fixed `w=1`, delay-`1`, `d=1`, `r=0` edge as the relay
input. Record/reconcile source external events, source configuration,
canonical emission identities/times/payloads, edge, routed event and relay
reception. The actual input sequence feeds the analytic ACP-0008 oracle.
Do not compensate for source state, rewrite payloads, or use a magic
`0.40000088897` fixture value.

## Exactness and numerical policy

Exact comparisons apply to candidate values and selected candidate;
stimulus schedule; event count, identity, order and one-to-one provenance;
relay emission count and direct/integrated/none classification; control
enablement; route/reception event identity and payload copy; and serialized
replay records/digests on the same execution environment.

For independent floating equation checks only, use the predeclared bound:

`tol(a,b) = 64 * sys.float_info.epsilon * max(1.0, abs(a), abs(b))`

Apply this to recomputation of source emission amplitude, Model-B transform,
ACP-0008 `z` recurrence and analytic oracle, plus floating neutral-return
checks. The bound is a conservative binary64 rounding allowance for the
small fixed sequence of elementary-function, multiplication, addition,
clipping and subtraction operations. Record the Python/platform/float
identity and maximum residuals. It is not a task tolerance, is not fit to
the Luna-41 residual, and cannot waive any exact count, causal identity,
classification, candidate, or selection criterion. The actual relay
reception value must equal its corresponding queued routed payload exactly;
its expected Model-B value is independently recomputed under the stated
floating tolerance.

## Provenance and gates

Luna-42 must begin implementation at the published authorization revision.
Before experiment execution, publish the owned runner/tests/configuration as
a commit, fetch `origin`, and start the experiment from clean synchronized
`main` at that committed runner revision (`HEAD == origin/main`). Before
running, record non-null `git rev-parse HEAD`, verify the runner is tracked
by that commit, and capture the runner SHA-256, configuration digest,
Python/platform/float metadata and repository status.
Every primary JSON artifact (`config.json`, Phase-A freeze, `results.json`,
and `summary.json`) must contain the same provenance envelope: execution
revision, runner identity/hash, configuration digest, artifact digest and
replay identity. Compute config digest over the frozen config object without
the provenance envelope.
Verify the source revision and runner hash again before Phase-B stream
creation and at completion. Missing or inconsistent provenance is a
**BLOCKED** stop condition, not a substitute for recorded revision.

Compute each artifact digest over canonical serialized content with its own
digest field omitted; record the canonicalization and SHA-256 algorithm.
Also retain an aggregate run digest to bind the artifacts together.

Run and replay every Phase-A candidate/fixture twice from reset. Select only
from exact discrete Phase-A outcomes according to the original rule. Freeze
and hash complete Phase-A records and the selected candidate before any
Phase-B stream helper is called. If no candidate passes every fixture, or
any provenance, source-emission, routing, equation, control, bounds or
replay check fails, record a null selection and do not run Phase B.

If Phase A validly selects a candidate, Phase B uses the unchanged
unlabeled five-seed/64-sequence fixture, the fixed ordinary
`source -> relay -> destination` `w=1` topology, and Luna-41's exact resource
bounds. Compare calibrated, default (`0.1`) and disabled relay arms with
identical source input streams. Phase B is descriptive only; it cannot
modify selection or parameters. Record ordinary relay emissions and any
onward routed transfers independently. No destination emission, efficacy,
accuracy, structural-growth benefit, energy benefit, hardware equivalence,
optimality or promotion claim is authorized.

## Architecture and governance

No ACP or Architecture Contract change is proposed. ACP-0008 stays
**experimental / opt-in / unpromoted**; ACP-0007 stays unchanged and
disabled. WEMA is only an unresolved alternative architecture idea and is
not authorized for implementation or experiment while the fixed exponential
model awaits a valid corrective test.

Luna-42 is the sole bounded successor authorized here. It must not be
executed as part of this decision. Return its complete handoff and evidence
to Luna-0 for independent review. This governance-only pass does not rerun
the full test suite; the previously reviewed baseline is 1015 passed,
1 skipped, 1016 collected (CUDA unavailable). `git diff --check` is required
for this publication. Luna-42 must run focused tests, the full repository
suite, and report exact counts and skip reasons.
