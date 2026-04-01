# Error-Driven Training Loop

## Objective
Minimize prediction error over time.

## Loss
L = (x_{t+1} - y_t)^2

## Algorithm

Initialize:
- y
- reservoir state R
- parameters θ

Loop over time:

1. Compute error:
   ε_t = x_t - y_{t-1}

2. Update reservoir:
   R_t = Reservoir(R_{t-1}, ε_t)

3. Compute gain:
   α_t = f_θ(R_t)

4. Update prediction:
   y_t = y_{t-1} + α_t * ε_t

5. Compute future error:
   δ_t = y_t - x_{t+1}

6. Update parameters:
   θ ← θ - η * δ_t * (ε_t)

## Notes
- Fully online
- No BPTT required
- Stable due to local updates
