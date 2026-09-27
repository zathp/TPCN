# Voice Recognition as an Updateable Baseline Skill

## Overview

Voice recognition should sit in the same adaptive baseline layer as face recognition.
It should begin with stable low-level auditory primitives, form reusable speaker embeddings, and update slowly as a person's voice changes over time.

This gives the brain model a second identity channel that can reinforce or challenge visual recognition.

---

## Pipeline

A practical voice-recognition pipeline inside this architecture is:

1. fixed auditory primitives detect pitch bands, harmonics, onset structure, rhythm, and spectral shape
2. adaptive baseline voice modules group these over short temporal windows
3. a speaker embedding is formed from stable vocal traits
4. the embedding is compared against stored speaker prototypes
5. high-confidence stable matches update the speaker prototype slowly

---

## Baseline Voice Representation

For each observed voice segment, define an embedding vector $v_t$.

This embedding can include:

- fundamental frequency statistics
- formant structure
- timbre envelope
- speaking cadence
- pause timing patterns
- articulation style
- channel-normalized spectral features

The goal is to preserve identity-related vocal structure while reducing dependence on the exact spoken content.

---

## Speaker Prototype Memory

Each known speaker can maintain a prototype vector $u_j$.

Recognition can be based on similarity:

$$
r_j = \frac{v_t \cdot u_j}{\lVert v_t \rVert \lVert u_j \rVert}
$$

and the winning speaker is:

$$
j^* = \arg\max_j r_j
$$

provided the score clears a confidence threshold.

---

## Update Rule

When speaker recognition is confident across a stable temporal window, the prototype can be updated slowly:

$$
u_j \leftarrow (1 - \lambda) u_j + \lambda v_t
$$

with small $\lambda$.

This allows the model to absorb:

- microphone variation
- room acoustics
- mood-related speaking shifts
- gradual aging effects
- health-related voice changes

without erasing identity too quickly.

---

## Temporal Windowing

Voice identity is often less reliable at a single instant than face identity.
It should therefore update over short sequences rather than isolated frames.

Example requirement:

- accumulate evidence across multiple audio windows
- require consistent speaker match over those windows
- reject updates during strong noise or overlapping speech

This makes speaker memory more robust.

---

## Interaction With The Personal Anchor

The adaptive voice baseline provides:

- speaker embeddings
- familiarity scores
- novelty flags
- timing and cadence summaries

The personal anchor then answers the stronger question:

is this specifically your voice, and does it align with the historically imprinted vocal pattern

This preserves the distinction between general speaker recognition and personal identity grounding.

---

## Interaction With Other Modalities

Voice recognition should not operate alone.
It should be compared against:

- face recognition
- contextual identity expectation
- emotional state inference
- temporal continuity of interaction

Agreement across modalities should raise confidence.
Disagreement should reduce update strength.

---

## Spatial And Temporal Layout

Voice recognition is not spatial in the same way as face parts, but it still benefits from structured local organization.

Example local groups:

- low-frequency pitch groups
- mid-band formant groups
- onset and consonant transition groups
- cadence and pause timing groups
- long-window speaker style groups

These can be arranged as local temporal-frequency neighborhoods that connect efficiently inside the adaptive baseline layer.

---

## Failure Modes To Guard Against

The system should avoid updating speaker identity when:

- multiple voices overlap
- the signal is clipped or heavily compressed
- background noise dominates
- the utterance is too short
- emotional distortion temporarily masks stable identity features

These conditions should lower the update gate even if the current best match looks plausible.

---

## Outcome

Voice recognition should be treated as an updateable baseline skill parallel to face recognition.
That gives the architecture a reusable auditory identity mechanism that improves over time, supports the personal anchor, and provides a second strong path for stable person recognition.