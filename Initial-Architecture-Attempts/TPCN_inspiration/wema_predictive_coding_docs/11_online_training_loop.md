# Online Training Loop (No BPTT)

## Goal
Train α generator using streaming prediction error.

## Loss
L = (y_t - x_{t+1})^2

## Update Signal
δ_t = y_t - x_{t+1}

## Algorithm

Initialize:
- reservoir state R
- output y
- parameters θ

Loop over time:

1. Update reservoir:
   R_t = ReservoirStep(R_{t-1}, x_t)

2. Compute α:
   α_t = f_θ(R_t)

3. WEMA update:
   y_t = α_t * x_t + (1 - α_t) * y_{t-1}

4. Compute error:
   δ_t = y_t - x_{t+1}

5. Parameter update:
   θ ← θ - η * δ_t * ∂y_t/∂θ

## Key Insight
Only local gradients needed:
∂y_t/∂α_t = (x_t - y_{t-1})

So:
θ update depends on:
(x_t - y_{t-1}) * δ_t

## Benefits
- No backprop through time
- Fully streaming
- GPU friendly
