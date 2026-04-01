# Cross-Modal Person Identity Fusion

## Overview

Face and voice recognition should not remain separate forever.
The brain model needs a fusion layer that combines identity evidence across modalities into a single person hypothesis.

This fusion layer should:

- merge supporting evidence from multiple channels
- detect contradiction between channels
- decide when identity is stable enough to update memory
- provide a unified identity estimate to the personal anchor and open reservoir

---

## Inputs To Fusion

At minimum, the fusion layer should receive:

- face identity scores
- voice identity scores
- temporal continuity signals
- contextual expectation signals
- current anchor agreement
- overall predictive error level

These are not all equally reliable at every timestep.
Fusion must therefore be confidence-weighted.

---

## Person Hypothesis

Let each candidate identity be indexed by $j$.

Define:

- $s_j^{face}$ as the face similarity score
- $s_j^{voice}$ as the voice similarity score
- $c_t$ as contextual support
- $a_t$ as anchor agreement

Then a simple fused score can be written as:

$$
F_j = w_f s_j^{face} + w_v s_j^{voice} + w_c c_t + w_a a_t
$$

where the weights depend on current signal quality.

The winning person hypothesis is:

$$
j^* = \arg\max_j F_j
$$

provided the fused score and its margin are both large enough.

---

## Confidence Weighting

The modality weights should adapt to sensory conditions.

Examples:

- if the face is occluded, reduce $w_f$
- if audio is noisy, reduce $w_v$
- if context strongly predicts one person, raise $w_c$ cautiously
- if anchor agreement is high, increase the stabilizing effect of $w_a$

This prevents the fusion layer from trusting the wrong channel at the wrong time.

---

## Agreement And Contradiction

Fusion must explicitly model both agreement and contradiction.

### Agreement Case

If face and voice both support the same identity, confidence should rise quickly.

### Contradiction Case

If face and voice support different identities, the system should not collapse immediately to one answer.
It should enter a contested state.

In that state, the model can:

- postpone baseline updates
- request more evidence across time
- use temporal continuity to resolve ambiguity
- allow the open reservoir to reason about explanation candidates

Examples of explanations:

- wrong visual match
- wrong speaker match
- dubbed or replayed audio
- two people in the same scene
- one visible person and another off-screen speaker

---

## Temporal Fusion

Identity should not be fused from a single instant only.

Maintain a running person hypothesis $h_t$ over time:

$$
h_t = (1 - \beta) h_{t-1} + \beta \hat{h}_t
$$

where $\hat{h}_t$ is the instantaneous fusion result and $\beta$ controls update speed.

This allows identity certainty to accumulate gradually.

---

## Update Gate For Identity Memory

A person memory should update only when the fused hypothesis is stable.

Example gate inputs:

- fused confidence is above threshold
- top identity margin is above threshold
- modality contradiction is low
- anchor agreement is sufficient
- global predictive error is not in a chaos regime

Only then should the associated face and voice prototypes be allowed to adapt.

---

## Unknown And Novel Persons

If the fused evidence does not strongly support any known identity, the model should form a provisional unknown person hypothesis.

This should:

1. hold linked face and voice observations together when possible
2. avoid contaminating known identities
3. become a stable identity only after repeated confirmation

This is important because person identity is stronger than any single modality alone.

---

## Interaction With The Personal Anchor

The personal anchor should consume the fused person hypothesis, not just individual face or voice scores.

That lets the anchor answer questions like:

- is this you
- is it probably you but with degraded sensing
- is one modality claiming you while another contradicts it

This makes the anchor more robust and less likely to overreact to one noisy channel.

---

## Interaction With The Open Reservoir

The open reservoir should receive:

- fused identity confidence
- contradiction flags
- novelty flags
- unexplained mismatch signals

This lets the reservoir model social ambiguity and anomaly without directly overwriting baseline identity memory.

---

## Spatial And Structural Interpretation

The fusion layer does not need to be fully spatial in the same way as raw perception modules.
But it should still be structured.

A practical organization is:

- modality-specific baseline modules produce embeddings and scores
- a compact multimodal identity layer integrates them
- the anchor and reservoir read out from this compact person-state representation

This keeps fusion computationally smaller than raw perception while preserving interpretability.

---

## Final Insight

Person identity should be treated as a fused latent state, not a single-sensor guess.

That gives the architecture three important properties:

- stronger recognition under partial information
- safer behavior when modalities disagree
- cleaner gating for online memory updates

This is the missing link between adaptive baseline skills and a coherent self-other model.