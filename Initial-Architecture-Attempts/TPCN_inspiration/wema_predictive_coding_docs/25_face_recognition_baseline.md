# Face Recognition as an Updateable Baseline Skill

## Overview

Face recognition should be treated as a baseline cognitive structure that can improve over time.
It should not be fully hardcoded, and it should not require the entire open reservoir to rediscover identity from scratch.

---

## Pipeline

A practical face-recognition pipeline inside this architecture is:

1. fixed visual primitives detect edges, symmetry, orientation, and local contrast
2. adaptive baseline face modules group these into facial parts
3. a face embedding is formed from stable geometry and appearance cues
4. the embedding is compared against identity prototypes
5. confident repeated matches update the stored prototype slowly

---

## Baseline Face Representation

For each observed face, define an embedding vector $f_t$.

This embedding can include:

- coarse head shape
- eye spacing
- nose-mouth geometry
- skin-tone statistics
- temporal movement style
- expression-normalized identity cues

The system should separate identity from expression as much as possible.

---

## Identity Prototype Memory

Each known identity can maintain a prototype vector $m_j$.

Recognition score can be based on similarity:

$$
s_j = \frac{f_t \cdot m_j}{\lVert f_t \rVert \lVert m_j \rVert}
$$

or another bounded similarity measure.

The winning identity is:

$$
j^* = \arg\max_j s_j
$$

provided that the score exceeds a confidence threshold.

---

## Update Rule

When the identity match is confident and stable over multiple frames, the prototype can be updated slowly:

$$
m_j \leftarrow (1 - \lambda) m_j + \lambda f_t
$$

with small $\lambda$.

This allows the model to absorb:

- aging
- lighting changes
- hairstyle changes
- viewpoint variation
- gradual camera-domain variation

without rewriting identity memory too quickly.

---

## Temporal Stability Requirement

A single frame should usually not update identity memory.
The update should require temporal agreement.

Example rule:

- match the same identity for $K$ consecutive steps
- require similarity above threshold for most of those steps
- require low contradiction from other modalities

Only then allow the prototype update.

---

## Interaction With The Personal Anchor

The face-recognition baseline does not replace the personal anchor.
It serves the anchor.

The baseline layer provides:

- stable identity embeddings
- familiarity scores
- novelty flags
- part-level facial structure

The anchor then answers the stronger question:

is this specifically you, and does it match your historically imprinted pattern

---

## Interaction With The Open Reservoir

The open reservoir should receive face embeddings and mismatch signals, not raw identity memory updates.

This lets it reason about:

- social context
- novelty
- expectation violation
- interpersonal comparison

without destabilizing baseline perception.

---

## Spatial Layout

Face recognition maps naturally onto spatial localism.

Example region groups:

- upper-face neurons
- eye-pair relation neurons
- nose bridge neurons
- mouth contour neurons
- outline and pose neurons

These local groups can register on the same grid system and form structured neighborhoods for fast part-based matching.

---

## Outcome

Face recognition should be an updateable baseline skill that sits between raw vision primitives and high-level identity memory.
That gives the architecture a reusable perceptual skill that can improve without becoming unstable.