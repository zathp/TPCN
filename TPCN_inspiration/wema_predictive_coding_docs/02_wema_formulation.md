# WEMA Formulation

## Basic Equation
y_t = α_t x_t + (1 - α_t) y_{t-1}

## Learnable Component
α_t can be:
- Constant
- Time-varying
- Neural-network generated

## Interpretation
α_t acts as a dynamic trust factor between:
- New data (x_t)
- Memory (y_{t-1})
