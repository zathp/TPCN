# Self and Other Boundary Inference

## Overview

Once the system can recognize identity and facial state, it still needs a more fundamental judgment:

- is this me
- is this a known other
- is this an unknown other

This should be handled by a dedicated self/other boundary inference layer.

That layer sits downstream of identity fusion and upstream of high-level action, memory update, and self-model reasoning.

---

## Why A Separate Boundary Layer Is Needed

Identity recognition alone is not enough.

A system may recognize a face or voice strongly, but still need to know whether that signal belongs to:

- the self anchor
- a familiar external person
- an unfamiliar external person
- an ambiguous or contested source

The self/other boundary layer provides this categorical separation.

---

## Inputs To Boundary Inference

The boundary layer should receive:

- fused person identity hypothesis
- anchor similarity and agreement
- face and voice confidence
- facial-state or behavioral state summaries
- temporal continuity
- perspective and sensor-origin cues
- global predictive error

These inputs let the model distinguish not just who is present, but how that presence relates to the self-model.

---

## Boundary States

A practical set of boundary classes is:

- self
- probable self
- familiar other
- unknown other
- contested or unresolved

These are more useful than a hard binary because real sensing is uncertain.

---

## Boundary Score Model

Let:

- $I_t$ be fused identity confidence
- $A_t$ be anchor agreement
- $P_t$ be perspective-consistency score
- $E_t$ be global error level

Then a self score can be written as:

$$
B_{self} = w_I I_t + w_A A_t + w_P P_t - w_E E_t
$$

and analogous scores can be built for familiar other and unknown other.

The boundary state is then selected from the highest valid score, subject to margin and stability constraints.

---

## Perspective Consistency

The system should use perspective cues when available.

Examples:

- does the perceived face come from a mirror-like configuration
- does the voice timing align with internally generated speech or expected self-speech
- does the body position match self-centered motion expectations

These cues are important because a strong identity match alone may still be insufficient to conclude self.

---

## Temporal Stability

Boundary inference should accumulate over time rather than oscillate instantly.

Use a smoothed boundary state:

$$
b_t = (1 - \rho) b_{t-1} + \rho \tilde{b}_t
$$

where $\tilde{b}_t$ is the instantaneous boundary estimate.

This prevents unstable flipping between self and other under noisy sensing.

---

## Interaction With The Personal Anchor

The personal anchor should not merely ask whether an identity resembles you.
It should read the boundary layer's output.

This lets it distinguish:

- confirmed self
- possible self under degraded sensing
- strongly familiar other who is not self
- unresolved source needing more evidence

That is critical for avoiding self-other confusion.

---

## Interaction With Memory Update

Boundary state should gate memory updates.

Examples:

- if boundary is self, allow cautious updates to self-related anchor traces
- if boundary is familiar other, route updates to that person's memory only
- if boundary is unknown other, create provisional external records
- if boundary is contested, freeze identity updates until evidence improves

This keeps the memory system properly partitioned.

---

## Interaction With The Open Reservoir

The open reservoir should receive boundary-state summaries such as:

- self certainty
- other certainty
- novelty flag
- contested-boundary flag

This lets the reservoir reason about social dynamics and ambiguity without directly collapsing self and other representations together.

---

## Failure Modes To Guard Against

The system should resist self/other confusion under conditions such as:

- mirrors and reflections
- delayed or replayed self audio
- recordings of known people
- multimodal contradiction between face and voice
- appearance changes that lower identity confidence

These cases should increase the contested-boundary state rather than force a premature decision.

---

## Final Insight

The self-model should not be just a strong identity prototype.
It should be protected by a dedicated boundary inference layer.

That gives the architecture a safer structure:

- self remains distinct from familiar others
- unknown others can be represented without contamination
- ambiguous cases remain explicitly unresolved until more evidence arrives

This is the layer that turns multimodal identity recognition into a coherent self-versus-other model.