# Training Methods

## 1. Gradient Descent
θ ← θ - η ∂L/∂θ

## 2. Online Learning (Recommended)
θ ← θ - η δ_t ∂y_t/∂θ

## 3. Hebbian Approximation
Δα ∝ (x_t - y_{t-1})(x_{t+1} - y_t)

## Notes
Online updates are efficient and stable for streaming data.
