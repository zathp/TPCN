# Latency + Buffer-Based Loop Architecture

## Overview

This system combines:
- Reservoir propagation delay (continuous, spatial)
- Explicit buffer delay (discrete, programmable)

Together they form hybrid temporal loops.

---

## Unified Equation

s_t = Σ w_i * h_{t-τ_i}  +  Σ v_j * B_j(t)

h_t = (1 - β) h_{t-1} + β * (a s_t) / (1 + b |s_t|)

---

## Delay Types

### 1. Propagation Delay
- Emerges from spatial structure
- Wave-like, continuous
- Encodes geometry of time

### 2. Buffer Delay
- Explicit delay lines
- Discrete and controllable
- Encodes precise timing

---

## Buffer Implementation

class DelayBuffer:
    def __init__(self, delay):
        self.buffer = [0] * delay

    def push(self, x):
        out = self.buffer.pop(0)
        self.buffer.append(x)
        return out

---

## Hybrid Loop Behavior

Signal flow:
1. Error enters reservoir
2. Propagates spatially
3. Enters buffer
4. Returns after delay

This produces:
- structured loops
- deformable temporal dynamics

---

## Predictive Coding Integration

Use error signal:

ε_t = x_t - y_{t-1}

Instead of buffering h_t:
buffer ε_t

This enables:
- delayed error correction
- temporal credit assignment

---

## Multi-Delay Extension

Use delay banks:

delays = [1, 2, 4, 8, 16]

Each contributes:

s_t += w_k * B_k(t)

---

## Stability Mechanisms

1. Softsign activation:
   f(x) = (a x) / (1 + b |x|)

2. Temporal damping:
   h_t = (1 - β) h_{t-1} + β f(s_t)

3. Buffer decay:
   buffer.append(x * decay)

---

## Key Insight

This system learns:
"when information should return"

Not just:
"what information is"

---

## Interpretation

This is a:
- delay differential system
- spatiotemporal dynamical system
- hybrid analog-discrete time model

---

## Capabilities

- long-term memory via buffers
- spatial reasoning via propagation
- temporal pattern learning via loop timing
