# Local priority weighted lottery — v1

Decision date: 21 October 2026.
Owner direction: "lets add it", following the agreed rule of learned weighted selection within equal-priority local pools.

Status: added to the project as a versioned design and isolated, tested reference implementation. This is not an accepted core ACP, a production integration or a change to frozen M2D/M2E source/protocol. No neural qualification was run.

## Agreed rule
For a selected locality L and priority Pn, use only eligible local connection heads whose priority matches Pn:

C(L,Pn) = { i : locality(i)=L, priority(i)=Pn, i is ready in the selected timestamp bucket }

S(L,Pn) = sum of W_i(Pn), for i in C(L,Pn)

Pr(i goes next | L,Pn) = W_i(Pn) / S(L,Pn)

Weights belonging to another locality or priority class never enter that sum. These are service preference weights, separate from neuron/edge signal amplitudes.

## Version 1 reference choices
The following defaults make the prototype precise and can be reviewed before integration:

1. Chronological eligibility comes first: consider local heads with timestamp <= now, then select the oldest timestamp bucket.
2. Inside that bucket, lower numeric priority is higher priority; priority 0 is highest.
3. Only the selected priority class participates in its local weighted lottery.
4. Accept at most one head request per local connection. Multiple queued events from one connection cannot multiply that connection's lottery weight. The connection's own queue supplies its oldest unserved head.
5. Sort candidates by stable connection ID and event ID before mapping the random ticket.
6. Choose one winner. Selection neither deletes nor modifies any request; the caller commits service, removes the served head, and supplies the next pool.
7. Each new service decision has a new stable decision ID. Reusing an ID is allowed for replaying a decision, not for treating it as a new service transaction.

Earlier timestamps are never bypassed simply because a later event has a higher class/weight. This reference does not change E1's external-before-internal ordering rule. It accepts communication signal metadata only; any integration adapter must preserve the existing internal-event precedence rules or explicitly version and review an experimental departure.

## Learned-weight interface
Learning remains external to this module. Each request carries a nonnegative connection weight from a frozen externally trained model; the model ID is included in the returned decision.
The prototype consumes weights; it does not implement a trainer or claim the illustrative weights were learned.

Version 1 uses unsigned32-bit integer weights, allowing exact sums and rational probabilities. An external trainer may produce real-valued parameters, but a deployment artifact must declare its quantization scale, rounding policy, training provenance and exact model hash before use.
No ground-truth class label is a runtime API input. A model ID identifies the complete frozen weight artifact, rather than a supplied answer for the current example.

If the selected pool has positive total weight, zero-weight members have zero chance on that draw. If all its weights are zero, use equal effective weights of1 and record uniform_fallback=true. No silent negative/nonfinite-weight repair.

## Seeded replay
The algorithm identifier is local-priority-lottery-v1.
An unsigned64-bit seed keys HMAC-SHA256. The canonical random context contains:
- algorithm version;
- locality;
- selected logical timestamp encoded with float.hex (signed zero normalized);
- selected priority;
- caller-supplied decision ID.

The context does not consume a shared global generator stream. Request ordering and changes to out-of-pool requests do not perturb the local decision.
Replay requires the same context, candidate identities and weight/model snapshot. Changing the eligible pool or learned weights may change the winner.

The first eight digest bytes supply a64-bit draw. Rejection sampling avoids modulo bias. At most eight draws are attempted, then an explicit error stops selection; no arbitrary winner is substituted.
The choice mechanism is bounded and reproducible, not a cryptographic access-control or secrecy mechanism.

## Bounds and evidence
- Maximum64 request records supplied per call, enforced during iteration before unbounded materialization.
- Priority0..65535; weight0..4294967295; seed0..18446744073709551615.
- Each identifier1..128 characters.
- Finite nonnegative logical times.
- Maximum total weight64*(2^32-1), summed exactly as integers.
- Maximum8 rejection attempts.
- No network-wide state, neuron updates, event routing, queue deletion or online weight update.

Returned Decision records the pool snapshot, raw and effective weights, exact sum, ticket, seed/context, model ID, selected signal/connection, fallback and sampler attempt count.

These per-call limits do not establish a complete runtime memory/work budget. An integration must bound total decisions, queued heads, retained records, trained-model storage and actual service delay.

## Validation performed
15 standard-library unit tests passed in0.054 seconds; exit code0.
The tests cover locality/priority isolation, older timestamps, all candidate input permutations, irrelevance of out-of-pool changes, zero cases, invalid metadata, duplicate heads, selection without mutation, a finite seeded weighted-frequency check, rejection exhaustion, exact maximum sums and bounded consumption of an infinite iterable.
The4096-decision frequency check is a deterministic sampler regression, not a neural workload, learning benchmark or proof of improved task results.
Raw command output is saved in test-result.json; manifest.json binds the retained files by SHA-256.

## Remaining design/integration work
- Choose and evaluate the external learning objective: benefit of earlier service, predictive/task quality, waiting time and actual work should be measured separately. No particular objective/update rule has been adopted.
- Specify whether each locality represents a destination input arbiter, routing resource or another explicitly bounded physical/logical point.
- Define fairness across priority classes and maximum wait. Strict priority and positive lottery chances alone do not provide a general bounded-wait guarantee.
- Compare chronological/FIFO, uniform seeded arbitration, and learned weighted arbitration using held-out examples/seeds, without task labels entering runtime.
- Record and evaluate any physical service/transport delay; never relabel that delay away.
- Review how same-time signal ordering affects nonlinear neuron state. Do not characterize this policy as a behavior-preserving storage optimization.
- Integrate only through a newly reviewed scope with exact source/model/protocol identity.

The E1 same-timestamp rearm failure remains unresolved and separate. This module does not bypass it, alter its event accounting or authorize a qualification retry.

## Files
- arbiter.py: pure bounded reference selection.
- test_arbiter.py: tests.
- example-weights.json: illustrative, untrained input weights.
- test-result.json: actual command output.
- manifest.json: file identity ledger, excluding itself.
