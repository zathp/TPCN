# Multi-timescale WEMA

## Structure
Use multiple filters:
y_t^(i) = α_i x_t + (1 - α_i) y_{t-1}^(i)

Combine:
y_t = Σ w_i y_t^(i)

## Benefits
- Captures multiple time horizons
- Approximates convolutional kernels
- Improves predictive power
