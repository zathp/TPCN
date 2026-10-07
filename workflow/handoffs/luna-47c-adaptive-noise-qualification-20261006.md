---
tpcn_handoff:
  agent: "Luna-47C implementation worker; independent Luna-0 review pending"
  luna_identifier: "Luna-47C"
  descriptive_name: "Adaptive noise qualification and deadband"
  task_id: "luna-47c-adaptive-noise-qualification-20261006"
  component: "Isolated synthetic input qualifier"
  status: "predeclared - not executed"
  contract_version: "1.2"
  branch: "copilot/luna47c-investigation"
  base_revision: "789dda5988daf72f375d9713bd76a6da2b9e8b34"
  result_revision: "Outcome publication commit containing this handoff"
  dependencies: ["Luna-0 published authorization", "Luna-46 reviewed MIXED context only"]
  owner: "Project owner"
  classification: ["MECHANISM EXPERIMENT", "SYNTHETIC", "NOT EFFICACY"]
  hypothesis: "Robust target clipping reduces spike-induced envelope contamination and later suppression."
  counter_hypothesis: "Robust estimation still suppresses meaningful clusters or under-tracks noise."
  interfaces_relied_on: ["experiments/luna47c/PROTOCOL.md", "Qualifier.process(timestamp, raw)"]
  label_information_boundary: ["Truth is evaluator-only; no production imports or output feedback."]
  timing_assumptions: ["Strict increasing dyadic synthetic timestamps; event-local elapsed time; first dt=1."]
  reset_boundaries: ["Fresh B=0,N=.25,last_time=None per fixture, method and control."]
  resource_bounds: ["Three scalar state values plus immutable configuration; 16 fixtures x 240 events x 3 methods; matched controls."]
  authorized_scope: ["Fixed, adaptive and robust deadbands; synthetic scoring, replay, tests and publication."]
  unauthorized_scope: ["Accumulator, other lane consumption, production, topology, ACP, efficacy, merge, successor or promotion."]
  controls: ["Committed pre-outcome protocol", "Signal-free paired controls", "Exact sign mirrors", "Fixed tolerances and verdict gates"]
  measurements: ["False admissions, misses, baseline error/pull, noise contamination, recovery and sign symmetry"]
  information_boundary_check: ["Mechanism accepts time/raw only; truth mutation and source isolation tests planned."]
  hardware_mapping: ["Software binary64 only; no physical realization or equivalence claim."]
  architecture_invariants_touched: ["A01/A02 event-local state", "A07 truth isolation", "A08 finite bounds", "A15 portability not established"]
  preserves: ["All production/governance/topology files", "Luna-46 MIXED", "ACP-0007/0008 status"]
  architecture_change: false
  proposal: null
  files_changed: ["experiments/luna47c/", "tests/test_luna47c_qualification.py", "artifacts/luna47c/", "workflow/handoffs/luna-47c-adaptive-noise-qualification-20261006.md"]
  tests_added: ["Fixture coverage, truth isolation, exact equations, bounds, time/config validation, sign symmetry, contamination and replay"]
  tests_passing: []
  tests_failed: []
  tests_not_run: ["Focused, applicable regression and full suite: pending"]
  assumptions: ["Synthetic truth is injected-source presence, not threshold crossing."]
  unresolved: ["Scientific outcome and independent review pending"]
  recommended_next_agent: ["Independent Luna-0 review after pushed completion; no successor"]
---

# Luna-47C pre-outcome record

Protocol, fixtures, parameters, initialization/reset rules, numerical comparisons,
metrics and verdict gates are frozen in `experiments/luna47c/PROTOCOL.md`.
No scoring has been run at this stage. Outcome evidence will be committed
separately after this predeclaration commit.
