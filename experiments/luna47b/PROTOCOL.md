# Luna-47B predeclared gain-only protocol (2026-10-06)

Classification: downstream offline experimental mechanism / verification.
Hypothesis: deposition gain alone can make the retained DRIVE-LIMITED streams
reach their existing integration threshold. Counter-hypothesis: finite gain
cannot rescue them with the retained signed recurrence. No efficacy claim.

Checkout authorization: 789dda5988daf72f375d9713bd76a6da2b9e8b34.
Production/evidence baseline: 2cef8ea4b37a4ae586e3f383511cba63c9268ddc.
Use only the reviewed corrected Luna-46 artifact and its pinned Luna-44/45
sources. Verify the Luna-46 33-source integrity inventory, phase identities,
one-to-one raw enqueue/reception reconciliation, and exact reproduced
sequence objects before analysis. Preserve MIXED, category and stream identity.

For each character reset A=0; use every retained state-update boundary,
including non-reception updates, in retained order (queue order for ties).
Use exact timestamps/prior clocks, dt=t-prior_clock, rho=exp(-0.0125*dt),
tau=80, threshold=1, and unchanged z_max=4. At already-qualified successful
receptions E is the original signed routed payload; otherwise E=0.
Only deposition changes: A_input=clip(rho*A_previous+g_A*E, -4, 4).
No modification of upstream amplitudes, qualification, thresholds, decay,
routing, topology, fast state, predictive coding, or learning is made.

This is a **first integration-threshold boundary diagnostic**, not a
counterfactual full neuron/runtime simulation. Stop state evaluation at the
first abs(A_input)>=1, before any discharge/admission would affect future
state/events. Keep all remaining event inputs/identities but mark their
states censored/null. Do not disable discharge and then claim a neuron
trajectory, infer emissions, or reuse retained future inputs as if a modified
network had actually generated them. Saturation at that first boundary is
recorded. There is no artificial post-crossing trajectory.

Before choosing tested gains, derive the untriggered signed recurrence
B_i=rho_i*B_(i-1)+E_i, B_0=0. Before the first crossing, no clipping or
discharge occurs and A_i=g_A*B_i. Thus the mathematical critical gain is
1/max_i(abs(B_i)); if the maximum is zero report NO-CROSSING (infinite
required gain). Mixed signs do not break homogeneity; they must not be
converted to absolute-input accumulation. Float critical gains are rounded
estimates of the real boundary, not a guarantee of exact equality in binary64.

Domain: nonnegative finite gain, tested bound 1e6. Derive all gains first.
Global gain arms: baseline 1, then 0.99 and 1.01 times each of min, median
and max finite critical gain across all reception-bearing sequences, sorted
and deduplicated. Median is the middle element or arithmetic mean of the
two middle elements. Each sequence also gets its own 0.99/1.01 critical
bracket, including non-target categories. Never cap an out-of-domain gain
silently: fail/block execution. No outcome-driven sweep adjustment.

Numerics: binary64, math.exp; equation comparisons use
64*epsilon*max(1,abs(observed),abs(expected)). Inputs, identity, order,
timestamps, discrete threshold decisions, copied data, digests and replay
are exact. Source-code/protocol commit checks and published-artifact replay
comparison permit only exact Windows CRLF-to-LF checkout materialization;
retain both raw worktree and committed source hashes. Evidence files,
numerical values and artifacts are never rewritten or otherwise normalized.
If checkout text has CRLF, consume the immutable evidence Git blobs at the
declared production/evidence revision directly in memory, verify their exact
retained hashes and current blob identity, and record both committed and
checkout hashes/lengths. Permit only identical bytes or exact LF-to-CRLF Git
materialization in the checkout; any other mismatch blocks. No evidence file
is rewritten. The reviewed verifier's read-only byte loader is temporarily
bound to this committed-blob reader; its verification logic is unchanged.
Threshold comparisons have no tolerance. Bound states by 4;
validate finite inputs, dt, gains, deposits and states, at most 320 sequences,
512 update boundaries per sequence and 7 global arms. No random seed is used.

Metrics: all critical gains, event states/deposits/censoring, first crossings,
DRIVE-LIMITED rescue count/fraction (denominator 75), non-target crossings
(denominators 245 all other sequences and 33 other reception-bearing),
saturation, signs/cancellation and finite-state bounds. Report other-category
crossings as unintended for this target, not label errors or efficacy.
Physical interpretation is dimensional scaling only: charge/current or
resistor-ratio scaling at fixed C and leak RC, not measured circuit data.
Changing C alone changes tau and is excluded.

Verdict rule: BLOCKED for any integrity/replay/numerical/bound gate failure;
NOT SUPPORTED if no target is rescued by any legal tested gain;
PARTIALLY SUPPORTED if some but not all target streams are rescued;
SUPPORTED if all are rescued with decay/threshold/input invariance verified.
This verdict addresses only mathematical first-boundary gain sufficiency;
unintended crossings and physical realizability remain separate limitations.
Luna-46's MIXED verdict is never superseded.

Architecture: A01-A03 preserved by event-time/order/delay copying; A06-A07
production predictive/error/local learning untouched, analysis downstream;
A08 prefix bound/censoring prevents extrapolated unbounded dynamics;
A15 hardware-independent estimates only. No clause amendment or ACP.
Rollback: discard this lane's four owned path families, retain common base.
Next role: independent Luna-0 review after pushed completed handoff, no
integration, promotion, successor or further experiment authorized.
