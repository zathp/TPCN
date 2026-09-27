# Internal Normalization

## Compute Mean and Variance
μ_t = WEMA(x_t)
σ_t = WEMA((x_t - μ_t)^2)

## Normalize Input
x̃_t = (x_t - μ_t) / σ_t

## Benefits
- Stabilizes training
- Adapts to changing distributions
