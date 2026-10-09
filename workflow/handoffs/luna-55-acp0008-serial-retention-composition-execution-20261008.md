---
tpcn_handoff:
  agent: "Luna-55"
  luna_identifier: "Luna-55"
  descriptive_name: "ACP-0008 serial relay/destination retention composition"
  task_id: "luna-55-acp0008-serial-retention-composition-20261008"
  component: "Bounded EXCURSION_V1 E2 retained-input mechanism experiment"
  status: "complete - EXECUTED / PARTIALLY SUPPORTED; independent Luna-0 review pending"
  contract_version: "1.2"
  branch: "main"
  base_revision: "9fa35c87528ae2f7bae4dca2e0c9630dcb1947e1"
  result_revision: "8369c8e70209c553be0662b6d705177308151d68"
  dependencies:
    - "Luna-55 authorization and frozen selection: 312eba8c8e036927408fb2156756a50d15762bc8"
    - "Luna-53 destination-retention phases"
    - "Luna-54 relay-retention and historical-control phases"
    - "Authenticated Luna-45 source-to-relay events and Luna-46 zero-decay oracle"
  owner: "Project owner; next action is independent read-only Luna-0 review"
  classification:
    - "fixed 2x2 serial retention mechanism experiment"
    - "PARTIALLY SUPPORTED within the predeclared target and frozen software-reference setup"
    - "ACP-0008 remains experimental, opt-in and disabled by default"
  hypothesis: "On the 16 predeclared DRIVE-LIMITED streams whose exact Luna-54 relay-retention arrivals cross the signed zero-decay oracle, relay and destination retention together produce a complete-lineage destination discharge and linked canonical emission, while neither single-retention arm does."
  counter_hypothesis: "The composed finite-retention arm fails to respond selectively on the target, a single-retention arm also responds on target, a frozen negative control crosses, or the RR route/replay/recurrence/bounds audit fails."
  interfaces_relied_on:
    - "Authenticated Luna-45 source-to-relay E2 inputs and the existing bounded source-to-relay-to-destination path"
    - "Luna-53 destination-only retention phases and Luna-54 historical/relay-only phases"
    - "Luna-46 signed-prefix zero-decay oracle and frozen historical classifications"
  label_information_boundary:
    - "PASS: target/control strata are attached only after each stream execution; no label, target flag, or oracle output is a runtime input."
  timing_assumptions:
    - "Retained event timestamps and deterministic event ordering; no global neural timestep."
    - "Only relay and destination ACP-0008 decay_rate_z vary, each between 0.0125 and 0.00125."
  reset_boundaries:
    - "Fresh E2 state per stream, condition and phase; inherited source inputs and per-stream reset boundaries are unchanged."
  resource_bounds:
    - "320 streams, 1,715 source inputs per RR phase; queue capacity 128, runtime event budget 1,024, per-neuron event budget 4,096."
  authorized_scope:
    - "Execute and publish the already-authorized fixed HH/RH/HR/RR factorial; reuse authenticated retained cells only after both-phase compatibility checks."
    - "Run two fresh RR phases on the full causal path; retain complete phase records and downstream-only analysis."
  unauthorized_scope:
    - "No parameter search, alternate decay values, gain/payload/threshold/timing/topology changes, source rerun, training, task efficacy, production selection, hardware test, ACP/A01-A15 amendment, or successor experiment."
  controls:
    - "Authorization revision 312eba8c8e036927408fb2156756a50d15762bc8; execution runner/runtime revision ca378b216e962de2a81b0d3ada741867fa4b1fce; analysis revision 9fa35c87528ae2f7bae4dca2e0c9630dcb1947e1."
    - "All eight retained Luna-53/Luna-54 phase artifacts authenticated by Git blob and checkout SHA-256; both initial and replay preflight phases reconcile all 320 streams, 235 arrivals and 235 historical destination traces."
    - "The four factorial cells differ from HH only at the authorized decay paths: HH=.0125/.0125; RH=.00125/.0125; HR=.0125/.00125; RR=.00125/.00125 (relay/destination)."
    - "RR initial and replay use the same authenticated Luna-45 input digest, runner/config/source identities, and complete causal E2 path; no retained Luna-54 destination arrivals are injected."
  measurements:
    - "Primary target: 10/16 streams cross only in RR and have the predeclared SERIAL-INTERACTION signature; 6/16 do not cross. HH, RH and HR each cross 0/16."
    - "Target RR peak |z| spans 0.8747183546394985–1.2312161737416334; the 10 crossings exceed threshold 1.0. Target RR remains 0.07208666138788988–0.17037137800475688 below the signed zero-decay oracle peak."
    - "On the 16 targets, destination receptions are HH 33, RH 58, HR 33, RR 58; RR is the only arm with target responses."
    - "E+ zero-decay-insufficient 49, E0 10, NR1 189 and NR0 23 have zero destination crossings in every arm."
    - "Secondary temporal-retention stratum (33): crossings HH 0, RH 1, HR 19, RR 33; reported separately from the primary target."
    - "Across all 320 streams: destination receptions/emissions HH 235, RH 421, HR 235, RR 421; destination crossings HH 0, RH 1, HR 19, RR 43."
    - "RR route audit: 421 enqueued, 421 received, 421 matched, zero mismatches. RR initial/replay results match exactly."
    - "Independent recurrence audit passed for 1,715 relay and 421 destination updates; zero z-clipping events, zero pending events, and all stream resource limits passed."
    - "Route identity comparison between RH and RR passes on every stream."
  information_boundary_check:
    - "PASS: runtime receives only causal source events and fixed per-condition configurations; evaluator strata and zero-decay outputs are downstream-only."
  hardware_mapping:
    - "Not run; hardware realization is outside this authorized software-reference mechanism experiment."
  architecture_invariants_touched:
    - "No architecture/runtime implementation changes. Existing A01-A03 event-time causal execution, A07 evaluator isolation, A08 finite bounded dynamics and A15 portability boundary are relied upon but this experiment is not a conformance certification."
    - "No A01-A15 clause or ACP text amended; ACP-0008 remains experimental, opt-in and disabled by default."
  preserves:
    - "Luna-53 and Luna-54 historical scientific artifacts and accepted narrow mechanism findings."
    - "Luna-46 classifications, fixed stream partition and retained input evidence."
    - "No task efficacy, generalization, production/default, architecture-promotion or hardware claim."
  architecture_change: false
  proposal: null
  files_changed:
    - ".gitattributes (pin Luna-55 JSON artifact checkout to LF so recorded file SHA-256 values remain stable)"
    - "artifacts/luna55/rr-initial.json"
    - "artifacts/luna55/rr-replay.json"
    - "artifacts/luna55/summary-v2.json (superseded BLOCKED analysis; preserved)"
    - "artifacts/luna55/summary-v2-integrity.json (superseded analysis integrity catalog; preserved)"
    - "artifacts/luna55/summary-v3.json (authoritative analysis)"
    - "artifacts/luna55/summary-v3-integrity.json"
    - "workflow/handoffs/luna-55-acp0008-serial-retention-composition-execution-20261008.md"
    - "workflow/docs/luna/LUNA_WORKFLOW.md"
    - "workflow/ARCHITECTURE_CHANGELOG.md"
  tests_added: []
  tests_passing:
    - "python -m pytest -q tests/test_luna55_factorial.py: 6 passed."
    - "The related ten-module regression batch: 432 passed; the two failures are identified below and are not silent."
    - "Full repository run at 8369c8e70209c553be0662b6d705177308151d68: 1,715 tests passed and 1 skipped; the command as a whole failed on the five explicitly listed failures."
    - "Artifact self-digests and summary-v3 integrity catalog independently recomputed and passed; summary-v3 SHA-256 5f1bba890f00c117a019dccf39948ec9b2169579f3ce749c81c03edfd85a3f86."
  tests_failed:
    - "tests/test_luna53_retention.py::test_pinned_inputs_reconcile_without_running_neurons: legacy Luna-53 helper rejects the retained Luna-46 checkout SHA 542202...; expected literal 0d3292... is stale. Luna-55 verified the pinned Git object, checkout and embedded semantic digest without changing historical files."
    - "tests/test_luna46_depth_scaling_diagnostic.py::test_luna51_catalog_identity_is_pinned_to_the_expected_git_object: expected exact-Git-LF-to-CRLF checkout but observed exact materialization in this Windows checkout. No file or git configuration was changed."
    - "tests/test_luna47f_diagnostic.py::test_luna51_protocol_and_execution_code_keep_their_historical_git_identities, tests/test_luna47f_diagnostic.py::test_luna51_retained_artifact_hashes_reject_result_and_validation_substitution, and tests/test_luna47f_retained.py::test_reproduction_check_is_read_only: untouched retained Luna47F diagnostic bytes hash to aec4e589... while the legacy verifier expects f24a56bf...; the latter two failures cascade from that stale literal."
  tests_not_run:
    - "Independent Luna-0 review: pending; this handoff stops at that review gate."
    - "Task efficacy, hardware mapping, production suitability and architecture conformance: not authorized/not applicable."
  assumptions:
    - "Reused factorial cells remain valid only for the exact authenticated artifacts and both-phase compatibility checks recorded in summary-v3."
    - "Finite retention need not realize every zero-decay oracle prediction; the oracle is a selector, not an execution result."
  unresolved:
    - "An independent Luna-0 read-only review must assess the immutable publication, evidence lineage, stale raw-pin reconciliation, all analysis corrections and regression evidence."
    - "The 6/16 target noncrossings and 49 zero-decay-insufficient E+ controls remain unresponsive; no mechanism beyond this fixed comparison is authorized."
  recommended_next_agent:
    - "Luna-0 Architecture Guardian: independent read-only review of the final pushed publication; return PASS/BLOCKED with evidence and do not implement follow-on work."
---

# Luna-55 ACP-0008 serial retention composition — execution result

## Outcome and scope

**EXECUTED — PARTIALLY SUPPORTED within the fixed factorial and frozen
software-reference setup; independent Luna-0 review is pending.** The
authorized 2x2 experiment was completed without changing model/runtime source,
historical evidence, or any production interface. It reuses authenticated
HH/RH/HR evidence and freshly executes RR from retained Luna-45 source events
through the complete bounded E2 source→relay→destination path.

The four cells vary only ACP-0008 relay/destination `decay_rate_z`:

| Cell | Relay | Destination | Evidence |
|---|---:|---:|---|
| HH | 0.0125 | 0.0125 | Luna-54 control, initial and replay |
| RH | 0.00125 | 0.0125 | Luna-54 relay-retention intervention, initial and replay |
| HR | 0.0125 | 0.00125 | Luna-53 destination-retention intervention, initial and replay |
| RR | 0.00125 | 0.00125 | Fresh Luna-55 RR initial and replay |

Both-phase preflight reconciled all 320 streams, all 235 HH/HR arrivals, and
all 235 historical destination traces. All eight reused records are
authenticated in `summary-v3.json` by Git blob, checkout SHA-256, phase and
execution revision. The complete fresh RR records use identical runner blob
`ca97bf35273ff82b95eb20f9ebf7996c108f07c7`, runner SHA-256
`bf4eaad1614c94be50e7cac2bee0f32cc6ff15e4ea5bf0f22b1d84726c8db0ee`,
configuration digest `d99b31646791f37e9242dfb9089e299dc6ab31e21bc0f96b244e92a6f4bed708`,
and Luna-45 input digest
`d73c99d83847b50bb5cb66920b95c3546d818874f582b6b6d9d8c5bfa90aaa3b`.
Their E2/event-runtime/topology source identities are recorded in each phase
artifact and match across initial/replay.

## Observed results

**OBSERVED:** Of the 16 predeclared primary targets, 10 show a complete
RR-only target crossing (`SERIAL-INTERACTION`), while 6 do not cross. HH, RH
and HR each cross zero of 16. The target response is therefore selective in
this frozen setup, and neither single-retention arm alone reproduces it.
RR target peak absolute destination state ranges from
`0.8747183546394985` to `1.2312161737416334`; the ten crossings exceed the
fixed threshold 1.0. RR peaks remain below the signed zero-decay oracle peaks
for all 16 targets, by `0.07208666138788988` to `0.17037137800475688`;
finite retention does not reproduce all oracle predictions.

| Frozen population | Count | HH | RH | HR | RR |
|---|---:|---:|---:|---:|---:|
| Primary zero-decay-sufficient target | 16 | 0 | 0 | 0 | 10 |
| E+ zero-decay-insufficient control | 49 | 0 | 0 | 0 | 0 |
| E0 | 10 | 0 | 0 | 0 | 0 |
| NR1 upstream-active | 189 | 0 | 0 | 0 | 0 |
| NR0 no-input | 23 | 0 | 0 | 0 | 0 |
| Secondary temporal-retention stratum | 33 | 0 | 1 | 19 | 33 |

The target receives 33 arrivals in HH and HR, versus 58 in RH and RR. Across
all 320 streams, destination reception/emission counts are HH 235, RH 421,
HR 235 and RR 421. All 43 RR destination crossings comprise the 10 target
responses and 33 secondary temporal responses; the secondary stratum is not
included in the primary claim.

**OBSERVED:** Each RR phase processes 1,715 source inputs and produces 421
relay emissions and 421 destination receptions. The route ledger reconciles
421 enqueued / 421 received / 421 matched with zero mismatches. RR initial
and replay stream records are exactly equal; the RH/RR route-identity
comparison passes for all streams. Independent recurrence checks pass for
1,715 relay and 421 destination updates. No z-clipping event or pending event
is observed. All streams stay within queue capacity 128, runtime event budget
1,024 and per-neuron budget 4,096; measured peaks are queue 19, runtime 48,
relay-neuron 36 and destination-neuron 13 events.

**INFERRED, narrowly:** the result supports serial sufficiency of these two
retention interventions for 10 of the 16 preselected streams, with neither
single factor crossing on those targets. It does not establish task benefit,
generalization, a globally useful policy, or causality beyond the fixed
retained source and route. Six selected targets remain uncrossed; the 49 E+
zero-decay-insufficient streams remain an explicit unresolved drive-limited
population.

## Provenance, failed attempts, and superseded analysis

- Authorization/selection publication: `312eba8c8e036927408fb2156756a50d15762bc8`.
- RR execution source revision: `ca378b216e962de2a81b0d3ada741867fa4b1fce`.
- Post-execution analysis/tooling revision: `9fa35c87528ae2f7bae4dca2e0c9630dcb1947e1`.
- Integrity manifest: `summary-v3-integrity.json`, analysis revision
  `9fa35c87528ae2f7bae4dca2e0c9630dcb1947e1`, execution revision
  `ca378b216e962de2a81b0d3ada741867fa4b1fce`, manifest artifact digest
  `9a84ea9b022f805078ed70f1a74b3b39a69ea555b1bbe3b9e1adca39cc82cb1c`.
- RR initial: file SHA-256
  `2043a03744af925345a34ee3e7e704914c35f13faf1e9175bab9c9e600ad8b8b`;
  internal artifact digest
  `402494efd10b62d22b2e0b5a5d6dce878c4c20460f41cdec2c64b9a6c571e576`.
- RR replay: file SHA-256
  `7445773d6907488501a90d97064ebece57ccb9b0508b75df3f54fbe9a0555085`;
  internal artifact digest
  `360c85b9ef511cc6c442df8b70be6646d2418bd6d7159954d9c6409378cc49b8`.
- Authoritative `summary-v3.json`: file SHA-256
  `5f1bba890f00c117a019dccf39948ec9b2169579f3ce749c81c03edfd85a3f86`;
  internal artifact digest
  `eee9c5f86d4692d654c3c660a79e629a8e3c45f4dc0b7ea9a0be6faf86532f22`.
  Recomputed internal digests pass for both RR records, summary-v3 and its
  integrity manifest. `.gitattributes` pins `artifacts/luna55/*.json` to LF
  so these recorded file hashes are stable across Windows checkouts.

**OBSERVED provenance discrepancy:** before any RR condition executed, the
first pre-treatment attempt stopped in the Luna-54 helper because its literal
Luna-46 raw SHA-256/length (`0d32926f...`, 2,337,377 bytes) did not match the
materialized pinned file (SHA-256
`54220205537184dadc26eba3c59f7e9b36f01db579fd895339728e089e313d51`,
2,337,376 bytes). The exact pinned Git blob
`9506369d97babf7bc0ef15ed52efb738dcdcd549`, checkout bytes and embedded
semantic digest `f72ba671f6d1618ab60cf81d85ac664395646de43c3ad77c226f41b9aa657628`
were independently verified. A Luna-55-side loader then authenticated those
identities, adapted the stale helper assertion only for this read, and
restored helper state; no Luna-46/Luna-54 file or scientific artifact was
edited. Review this bounded exception before interpreting the reused cells.
The phase records' `execution_worktree_dirty` flag is true because generated
Luna-55 outputs were untracked while phase artifacts were written; their
runner, configuration, E2, event-runtime and topology identities point to
the exact committed execution revision above.

Two analysis defects after RR execution were corrected without rerunning RR.
The first aggregation raised a `KeyError`; a subsequent
`summary-v2.json` is preserved as `BLOCKED` because its route-signature
comparison omitted fields. The audit was corrected to compare identical full
route fields; an independent comparison finds zero RH/RR route identity
mismatches. `summary-v3.json` is the authoritative corrected result.
The earlier `summary.json` is retained as preliminary, not authoritative.

## Architecture evidence and limits

No canonical neuron, runtime, topology, ACP or architecture contract changed.
The experiment relies on event-driven causal execution and local elapsed-time
integration (A01-A03), keeps evaluator information outside the runtime (A07),
and remains within finite queues/event budgets/state bounds (A08). A15
hardware portability was not tested. This is not an A01-A15 conformance
review, architecture promotion, ACP amendment, hardware equivalence, task
efficacy, or production-default recommendation. No Luna-56 is authorized.

## Validation record

| Command or procedure | Revision / environment | Observed result | Evidence |
|---|---|---|---|
| Eight retained phase pin checks and initial/replay factorial compatibility preflight | Execution source `ca378b216e962de2a81b0d3ada741867fa4b1fce` | PASS; both phases, 320 streams, 235 arrivals and 235 HH destination traces | `summary-v3.json` |
| RR initial and replay; full causal E2 execution | Execution source `ca378b216e962de2a81b0d3ada741867fa4b1fce` | PASS; 320 streams/1,715 inputs each; 421 routes each | `rr-initial.json`, `rr-replay.json` |
| RR replay, recurrence, routing, bounds, clipping and label isolation audits | Analysis `9fa35c87528ae2f7bae4dca2e0c9630dcb1947e1` | PASS | `summary-v3.json` and integrity catalog |
| `python -m pytest -q tests/test_luna55_factorial.py` | Analysis source `9fa35c87528ae2f7bae4dca2e0c9630dcb1947e1`; Windows/Python 3.11 | PASS; 6 passed | Focused Luna-55 factorial suite |
| Related 10-module Luna-55/Luna-53/Luna-54/Luna-46/Luna-45/E2/excursion/runtime/topology regression batch | Analysis source `9fa35c87528ae2f7bae4dca2e0c9630dcb1947e1`; Windows/Python 3.11 | 432 passed, 2 failed: legacy Luna-53 stale raw pin; Luna-46 expected CRLF but observed exact materialization | Pytest output retained in session; both failures documented above |
| `python -m pytest -q` | Publication `8369c8e70209c553be0662b6d705177308151d68`; Windows/Python 3.11 | 1,715 passed, 5 failed, 1 skipped; overall FAIL because historical Luna-46/47F/53 pin/materialization assertions fail | Exact failure summary retained in this handoff; no historical file or test was changed |
| Independent Luna-0 review | Final immutable publication | PENDING — required stop gate | New read-only review handoff |

## Reproduction and next assignment

The authenticated records and current runner/config are under
`artifacts/luna55/` and `experiments/luna55/`. The runner supports the
contracted preflight, RR phase execution and offline summary/audit commands;
see `experiments/luna55/protocol.json` and
`experiments/luna55/run.py`. Do not rerun a scientific phase to reproduce
analysis; use the retained RR records. Preserve the superseded
`summary-v2.json` as diagnostic history.

Next assignment: **Luna-0 Architecture Guardian**, read-only review of the
final pushed revision and every Luna-55 phase/summary artifact, including the
stale Luna-46 raw-pin reconciliation, the preserved blocked summary-v2,
route/recurrence/bounds/label-isolation audits, and test evidence. Return
PASS/BLOCKED with exact findings. No implementation or successor experiment
is included in that assignment.
