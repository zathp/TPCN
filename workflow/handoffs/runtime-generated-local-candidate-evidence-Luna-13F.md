# Luna-13F execution resumption handoff

**BLOCKED - FIXTURE/ORACLE EVIDENCE CONTAMINATION**

```yaml
tpcn_handoff:
  agent: Luna-13F
  luna_identifier: "Luna-13F"
  descriptive_name: "Runtime-generated local candidate evidence resumption audit"
  task_id: "runtime-generated-local-candidate-evidence-Luna-13F"
  component: "Preserved untracked CPU prototype, independent counterexamples and handoff"
  status: "blocked"
  contract_version: "1.1"
  branch: "main"
  base_revision: "f0821bd5eb0441ea892c463cbbcf173c80d09be6"
  result_revision: "uncommitted resumption repair; blocked prototype preserved in backup"
  dependencies: ["Luna-13B", "Luna-13C", "corrected Luna-13D", "independently reviewed Luna-13E"]
  owner: "Luna-0 independent review"
  classification: ["EXPERIMENT", "VERIFICATION", "CPU-only"]
  hypothesis: "Existing runtime events produce local bounded evidence predicting the narrow G/H distinction."
  counter_hypothesis: "Evidence depends on fixture roles, unequal exposure or future observations."
  interfaces_relied_on: ["TPCNNeuron", "TemporalAssociationPolicy", "CandidateEvidence", "StructuralPlasticityController", "execute_bounded"]
  label_information_boundary: ["Labels and held-out results must remain evaluator-only; role contamination is observed."]
  timing_assumptions: ["Finite event timestamps; current prototype lacks a fixed structural-decision freeze."]
  reset_boundaries: ["Fresh neuron and association policy per run; held-out cases reset to time zero."]
  resource_bounds: ["32-event primary budget", "queue 16", "history 8 per node", "candidate capacity 2", "maximum score 8", "edge capacity 3", "fan-in 2", "fan-out 1"]
  authorized_scope: ["Existing unfinished Luna-13F audit, bounded reproduction, artifacts, handoff"]
  unauthorized_scope: ["New architecture semantics", "A14 promotion", "Luna-13G", "hardware execution", "discarding user work"]
  controls: ["Matched exposure", "future-only mutation", "budget exhaustion", "equalization", "no-evidence", "chronology", "score reconstruction", "replay"]
  measurements: ["Source hashes", "event counts", "decision time", "score", "admission", "completion", "task outcome"]
  information_boundary_check: ["Failed: beneficial/harmful configuration selects evidence timing and frequency."]
  hardware_mapping: ["CPU verification only; no new hardware-relevant semantics implemented."]
  architecture_invariants_touched: ["A02", "A07", "A08", "A14"]
  preserves: ["Canonical production files and contract unchanged", "All five original files byte-preserved in the verified backup"]
  architecture_change: false
  proposal: null
  files_changed: ["tpcn/runtime_generated_evidence.py", "run_runtime_generated_evidence_13f.py", "tests/test_luna13f_runtime_generated_evidence.py", "artifacts/runtime-generated-local-evidence-13f-verified/", "artifacts/runtime-generated-local-evidence-13f/resumption-audit-20260930/audit_luna13f.py", "artifacts/runtime-generated-local-evidence-13f/resumption-audit-20260930/audit-results.json", "workflow/handoffs/runtime-generated-local-candidate-evidence-Luna-13F.md"]
  tests_added: ["Standalone reproducible contract audit; no original tests modified"]
  tests_passing: ["Focused 8", "Full CPU 284 with 1 skip", "Audit preservation and 5 contract observations", "Current source in-memory compilation"]
  tests_failed: ["Audit 8 contract checks, detailed below"]
  tests_not_run: ["Missing controls listed below", "Editor diagnostics", "Hardware validation"]
  assumptions: ["Original artifacts describe a prototype, not validated successful Luna-13F evidence."]
  unresolved: ["Valid ordinary-runtime evidence fixture", "Fixed freeze and held-out chronology", "Control completeness", "Truthful runner gating"]
  recommended_next_agent: ["Luna-0 independent review of this blocked result"]
```

## Provenance and preservation

**OBSERVED:** On the authorized MSI machine the three source files were untracked:
`tpcn/runtime_generated_evidence.py`, `run_runtime_generated_evidence_13f.py`,
and `tests/test_luna13f_runtime_generated_evidence.py`. Two untracked JSON artifacts
already existed. There were no tracked or staged changes. HEAD and origin/main were
`f0821bd5eb0441ea892c463cbbcf173c80d09be6`; committed tree:
`f49d4c46d751abce52944b11fa005312c122974a`.
The parent checked the live remote at that revision. No sync operation changed this dirty tree.

**OBSERVED:** All five original files were copied byte-for-byte before adding this
audit to `C:\Users\zathp\Documents\programming\TPCN-Luna-13F-backup-20260930-143250`.
Their complete SHA-256 manifest is in the [audit result](../../artifacts/runtime-generated-local-evidence-13f/resumption-audit-20260930/audit-results.json).
Its manifest fingerprint is `745c33a6d3c3a869a6f5fd86a5e9e37064597d176e7f8b5df9dae2eb61ceee96`.
The original backup is identified by that manifest, while the resumed executable
source is identified by the current audit manifest. The runner, artifact status,
and focused regression test were subsequently repaired; no architecture or
workflow contract was changed.
No staging, commit, push, reset, clean, stash, pull or rebase was performed.

## Implemented work and blockers

**OBSERVED:** The prototype delivers addressed events to a real canonical neuron and
existing bounded temporal-association policy, transfers policy counts into
CandidateEvidence, and invokes the unchanged canonical controller. G and H are both
individually legal, with exactly one relevant free slot. The old 13E tuple helpers
are not the primary path. However, `_schedule` lines 101-105 choose short/long
endpoints using `beneficial_role` and `harmful_role`. G receives three observations
at 0.5, 1.5 and 2.5; H receives one at 6.0. Thus the informative timing/frequency
is fixture-role assigned before runtime. Passing it through a neuron does not
remove the prohibited information source. Neuron residual/eligibility is diagnostic;
the count score does not depend on those fields.

**OBSERVED:** Primary G/H scores are 3/0; G is selected. The preserved evaluator
reports no-growth 2/2 at 8 events/8.0 proxy energy, G 2/2 at 12/12.0 and H 1/2
at 12/12.0. These reproduce reference task behavior but do not validate F's
evidence origin. G provides neither task improvement nor resource benefit over
the no-growth reference. Proxy energy is uncalibrated activity cost.

| Contract check | Result | Actual evidence |
|---|---|---|
| Fixture-role-free evidence | failed | Beneficial/harmful flags drive the primary schedule. |
| Matched exposure | failed | G 3 observations, H 1. |
| Frozen future exclusion | failed | Appending only events at 7, 7.5, 9, 9.5, 11, 11.5, 13, 13.5 changes G/H 3/0 to 3/4; H wins and decision moves 6 to 13.5. |
| Incomplete evidence exclusion | failed | Budget 2 processes 2 events, leaves 6 pending, reports exhausted and still grows G. |
| Evidence equalization | failed | Named equalized control scores G 2, H 1; it is not a tie. |
| No-evidence opportunity | failed | Control removes both candidates; supplying both legitimate candidates at score zero instead selects H by canonical tie rule. |
| Held-out chronology | failed | Held-out timestamps start 0, earlier than decision 6; no explicit later phase offset is represented. |
| Score update provenance | failed | Reported updates are cumulative 1,2,3, while actual count deltas are 1,1,1. |
| Two legal candidates/one slot | passed | Both legal; one growth and edge-capacity rejection. |
| Deterministic replay | passed | Full in-memory result reproduces. |
| Compilation and preservation | passed | All three original Python files compile; all five original hashes match backups. |

**OBSERVED:** The original runner printed its positive terminal status unconditionally.
The resumed runner now reports the blocked terminal status from the artifact, and
the focused regression test asserts that classification. Original artifacts remain
preserved as historical prototype output.

## Controls and architecture audit

**OBSERVED:** Order reversal and relabeling preserve the supplied evidence preference.
The mirror control swaps timing exposure and selects H; it does not independently
mirror the external useful/harmful topology roles. Shuffle, reversal and uniform
controls execute, but inherit the invalid primary evidence construction and have
no sufficiently asserted analytic falsification expectations. The builtin future
control happens not to change scores yet advances the decision boundary to 10.

**OBSERVED:** External-label mutation and locality attack are missing. Saturation,
history eviction and reset stress, valid mirrored-role evidence and a runtime
neutral-decay sweep were not run. The count policy has no decay parameter; neuron
decay is available but unused in scoring. The blanket neutral-decay N/A must be
qualified to that count score or supplemented by the valid zero-neuron-decay
control. Prediction/error, real prior delayed reward and pre-admission route-cost
evidence do not drive this prototype. No such evidence was fabricated.

**INFERRED:** Current TemporalAssociationPolicy can accumulate bounded local event
counts, with bounded histories, score saturation, candidate-capacity rejection and
reset. The observed deficiency is this fixture's prohibited source of informative
events. This audit does not prove the architecture cannot support another valid
ordinary-runtime fixture; an architecture-change requirement is **not established**.
No architecture-change decision packet or new learning subsystem is justified by
this contamination result alone.

**HYPOTHESIZED:** An ordinary-runtime, matched-exposure fixture using existing
mechanisms may be possible. It must be specified without usefulness flags or
candidate-specific timing answers, and allowed to tie or fail.

## Validation and reproduction

**OBSERVED:** Parent baseline validation on the unchanged sources: focused F tests
8 passed; complete CPU suite 284 passed, 1 skipped in 9.27 seconds. This includes
the existing predecessor and Stage-0 coverage; no dedicated extra preservation
run is claimed. Original sources compile in memory, saved artifact replay matches
after removing generation-only provenance, and whitespace checks pass.
Editor diagnostic-provider checks were not run. CUDA is optional and non-gating;
GPU/FPGA/FPAA execution is outside this CPU-only scope.

Run the standalone audit from the repository root:
```text
python -B artifacts/runtime-generated-local-evidence-13f/resumption-audit-20260930/audit_luna13f.py
```
It writes only its adjacent audit-results.json and reports 5 passed, 8 failed and
5 not-run audit records. These are contract-check classifications, not an added
pytest success count. Its temporary function patch is restored in process; it
does not edit the runtime source. After the scoped status repair, the focused
suite reports 8 passed and the full CPU suite reports 284 passed, 1 skipped.

## Next execution state

Return this blocked F result to Luna-0 for independent review. Unfinished F scope:
replace the role-keyed evidence schedule with a defensible existing-runtime
fixture or report a valid negative result; freeze at a declared decision event;
put held-out timestamps strictly later; exclude incomplete runs from successful
claims; implement the missing/invalid controls; reconstruct bounded score deltas;
and produce exact executed-source provenance and truthfully gated artifacts.
Then run focused adversarial checks and the contract's preservation matrix.

The authoritative workflow still records AUTHORIZED - LUNA-13F EXECUTION PENDING;
this handoff records the blocked attempt for Luna-0 reconciliation. No promotion
or positive evidence claim is made. Luna-13G was not created, authorized or dispatched.
