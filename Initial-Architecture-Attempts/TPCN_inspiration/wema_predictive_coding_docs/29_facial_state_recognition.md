# Facial State Recognition as an Adaptive Baseline Skill

## Overview

The system should not only recognize who a face belongs to.
It should also recognize what state that face is currently expressing.

This should be treated as a separate adaptive baseline skill from face identity.

Identity asks:

- whose face is this

Facial state asks:

- what is this face doing right now

Examples of facial state include:

- neutral
- smiling
- frowning
- surprise
- tension
- confusion
- fatigue
- pain-like strain
- attention focus

---

## Why It Must Be Separate From Identity

If facial state is mixed directly into identity memory, the model will confuse temporary expression with stable person structure.

The architecture should therefore keep:

- identity representation for persistent facial geometry
- facial-state representation for transient expression and condition

This separation is essential for stable recognition.

---

## Pipeline

A practical facial-state pipeline is:

1. fixed visual primitives detect edges, contours, symmetry breaks, and local motion
2. adaptive face-part modules estimate eyebrows, eyes, eyelids, mouth shape, jaw tension, and head pose
3. the system forms a facial-state embedding from these transient cues
4. the embedding is matched against state prototypes or state manifolds
5. temporal smoothing stabilizes the facial-state estimate across time

---

## Facial-State Representation

For each face observation, define a transient state vector $z_t$.

This vector can include:

- brow elevation or contraction
- eye openness
- gaze stability
- mouth curvature
- lip compression
- jaw openness or tension
- cheek lift
- head tilt and orientation drift
- micro-movement activity

Unlike identity memory, this representation is expected to change quickly.

---

## State Estimation

Let each facial state prototype be indexed by $k$.
Then a state score can be written as:

$$
q_k = \mathrm{sim}(z_t, e_k)
$$

where $e_k$ is a baseline representation for a facial state pattern.

The estimated facial state is:

$$
k^* = \arg\max_k q_k
$$

or a soft distribution across several states when ambiguity is high.

---

## Temporal Smoothing

Facial state should not flip violently frame to frame unless the face actually changes rapidly.

Use a smoothed estimate:

$$
\hat{z}_t = (1 - \gamma) \hat{z}_{t-1} + \gamma z_t
$$

with a moderate $\gamma$.

This keeps the state estimate responsive without turning every micro-noise fluctuation into a new state.

---

## Relation To Identity

Facial state should modulate identity confidence, not overwrite it.

Examples:

- smile changes mouth shape but should not erase identity
- fatigue changes eye openness but should not imply a different person
- pain or tension may distort normal face geometry, reducing identity confidence temporarily

So identity and facial state should exchange information but remain distinct.

---

## Relation To The Personal Anchor

The personal anchor should receive both:

- identity evidence
- facial-state evidence

This allows it to distinguish:

- this is you and you look calm
- this is you but your face shows stress
- this is likely you but expression distortion lowers confidence

This is important if the model is meant to read stable person identity and dynamic internal condition together.

---

## Relation To The Open Reservoir

The open reservoir should receive facial-state summaries as dynamic context.

This lets it reason about:

- interaction tone
- social tension
- mismatch between spoken content and visible expression
- prediction violations in behavior

The open reservoir should reason over the state, not store the state as a stable identity feature.

---

## Spatial Interpretation

Facial state maps naturally onto local face-part regions.

Useful local groups include:

- brow state neurons
- eyelid and eye-tension neurons
- mouth contour neurons
- cheek and lower-face tension neurons
- head-pose adjustment neurons

These can use the same spatial-grid registration logic already introduced for local structured lookup.

---

## Update Principle

Facial-state baseline structures should be adaptive, but not in the same way as identity prototypes.

They should update by improving the model of expression geometry and transition dynamics across many observations, not by locking a single moment into memory.

This means the module learns:

- what states exist
- how they deform facial parts
- how they transition over time

without confusing transient state with persistent identity.

---

## Final Insight

Facial state recognition should be a distinct adaptive baseline skill layered on top of face-part perception and alongside face identity.

That gives the system the ability to read dynamic facial condition while preserving stable identity memory.