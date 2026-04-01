# Adaptive Baseline Structures

## Overview

The brain model needs more than fixed primitives.
It also needs baseline structures that start simple, remain stable, and still update from experience.

Face recognition is the clearest example.

The correct split is:

- fixed primitives for universal low-level signals
- adaptive baseline modules for reusable perception skills
- anchor memory for person-specific imprinting
- open reservoir for broader world modeling

---

## Layer Revision

The original primitive layer should be interpreted as two sublayers.

### 1. Fixed Primitives

These are not learned online.
They act like built-in detectors.

Examples:

- edges
- symmetry
- motion onset
- pitch bands
- temporal rhythm
- intensity contrast

### 2. Adaptive Baseline Structures

These are initialized from generic structure, but they update gradually.
They are not fully open-ended memory and they are not frozen reflexes.

Examples:

- face recognition
- facial landmark grouping
- expression categorization
- speaker identity traces
- body posture templates

---

## Why A Separate Baseline Layer Is Needed

If face recognition lives only in the anchor layer, it becomes too personal and too rigid.
If it lives only in the open reservoir, it becomes too unstable and too diffuse.

The system needs a middle layer that can learn recurring structure while staying constrained.

That layer should answer questions like:

- is this a face at all
- which stable facial geometry is present
- how similar is this face to known identities
- is this a familiar identity with updated appearance

---

## Functional Role

Adaptive baseline structures should:

1. receive low-level features from fixed primitives
2. produce compact reusable perceptual embeddings
3. update slowly from repeated evidence
4. feed both the personal anchor and the open reservoir

This makes them shared perceptual infrastructure.

---

## Update Principle

These modules should update conservatively.

Let $b_t$ be the baseline state and $z_t$ the current perceptual observation.
Then a slow update can be written as:

$$
b_t = (1 - \eta_t) b_{t-1} + \eta_t z_t
$$

with small $\eta_t$.

Unlike open-reservoir adaptation, this is not meant to chase novelty quickly.
It is meant to accumulate stable regularities.

---

## Error Gating

Baseline structures should not update on every frame.
They should update only when:

- confidence is high enough
- sensory corruption is low enough
- identity match is stable enough across time
- global prediction error is not indicating chaos or contradiction

This prevents catastrophic drift.

---

## Spatial Interpretation

These baseline modules can also use the spatial grid.

For example:

- local spatial groups can represent eye, nose, mouth, and contour subfields
- nearby neurons can cooperate to encode stable facial geometry
- local neighborhoods can update feature clusters without global search

So the grid is not only for reservoir growth.
It can also support efficient perceptual grouping.

---

## Outcome

The architecture should now be read as:

- fixed primitives
- adaptive baseline structures
- personal anchor
- open reservoir

This gives the system a place for updateable perception skills such as face recognition without corrupting either the fixed reflex layer or the personal identity core.