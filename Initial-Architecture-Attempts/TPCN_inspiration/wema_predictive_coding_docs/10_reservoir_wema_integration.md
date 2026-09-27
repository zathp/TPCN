# Reservoir + WEMA Integration (Deep Dive)

## Core Concept
A spatial reservoir generates adaptive gain (α) for a WEMA update rule.

y_t = α_t x_t + (1 - α_t) y_{t-1}

Where:
α_t = Readout(Reservoir State)

## Interpretation
- Reservoir = nonlinear spatiotemporal encoder
- WEMA = stable integrator
- Combined = adaptive dynamical system

## Design Principle
Do NOT let the reservoir directly predict outputs.
Instead, it should control the dynamics (α).

## Spatial Formulation
Each voxel has:
- its own state
- its own α_t

α_t(x,y,z) enables:
- local adaptation
- turbulence tracking
- stable regions

## Multi-scale Extension
Multiple α fields:
y_t^(i) = α_t^(i) x_t + (1-α_t^(i)) y_{t-1}^(i)

Combine:
y_t = Σ w_i y_t^(i)

## Stability
Constrain α:
α = sigmoid(z)

Optional:
- temperature scaling
- clipping
