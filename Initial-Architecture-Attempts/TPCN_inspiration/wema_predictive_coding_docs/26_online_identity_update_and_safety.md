# Online Identity Update and Drift Safety

## Overview

Once baseline structures such as face recognition are allowed to update, the main risk is drift.

If the system updates too fast, it stops recognizing identities correctly.
If it never updates, it becomes brittle.

The architecture therefore needs explicit safety rules for online baseline updates.

---

## Core Rule

Identity memory should update only under agreement.

Agreement means consistency across:

- time
- sensory quality
- baseline confidence
- anchor confirmation
- global predictive stability

---

## Multi-Gate Update Condition

Let:

- $s_t$ be identity similarity score
- $q_t$ be face-quality score
- $a_t$ be anchor agreement
- $e_t$ be global error magnitude

Permit an update only if:

$$
s_t > \tau_s, \quad q_t > \tau_q, \quad a_t > \tau_a, \quad e_t < \tau_e
$$

for a stable temporal window.

This means the system updates only when the recognition is both confident and behaviorally coherent.

---

## Prototype And Exemplar Memory

A robust design keeps two forms of identity memory.

### 1. Prototype Memory

Compact running identity average.

### 2. Exemplar Buffer

A small memory of recent high-confidence observations.

The prototype captures stability.
The exemplar buffer captures variation.

This makes the system more resistant to overfitting one recent face condition.

---

## Controlled Update Rule

One safe pattern is:

$$
m_j \leftarrow (1 - \lambda g_t) m_j + \lambda g_t f_t
$$

where $g_t \in [0, 1]$ is an update gate derived from confidence and stability.

If confidence is weak, then $g_t$ stays near zero.
If confidence is strong and persistent, then $g_t$ opens slightly.

---

## Novel Identity Formation

If no known prototype matches strongly enough, the system should not force the face into the nearest existing identity.

Instead it should:

1. create a provisional unknown identity record
2. accumulate evidence across multiple encounters
3. promote it to a stable identity only after repeated confirmation

This avoids identity contamination.

---

## Recovery From Drift

The system should be able to detect when an identity model has drifted.

Warning signals include:

- sudden drop in match consistency
- growing disagreement with anchor memory
- strong contradiction from temporal context
- repeated reassignment between two identities

When this happens, the model can:

- reduce update rate
- fall back to exemplar comparison
- freeze the prototype temporarily
- rebuild from recent high-confidence exemplars

---

## Broader Baseline Skills

The same update-and-safety logic should apply to other baseline structures:

- voice recognition
- gait recognition
- expression recognition
- posture recognition
- hand-shape recognition

Face recognition is only the first instance of a more general adaptive baseline layer.

---

## Final Insight

Baseline perception should be plastic, but only under disciplined conditions.

That gives the brain model a practical middle ground:

- stable enough to keep identity intact
- flexible enough to adapt to real-world change
- structured enough to support long-term recognition

This is how updateable structures such as face recognition can fit into the predictive brain without corrupting the core self-model.