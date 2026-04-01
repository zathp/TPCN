# Predictive Coding Architecture (Formalized)

## Core Variables
x_t : input
y_t : prediction
ε_t : error

## Equations

Prediction:
y_{t-1}

Error:
ε_t = x_t - y_{t-1}

Update:
y_t = y_{t-1} + α_t ε_t

## Reservoir-driven Gain
α_t = f_θ(R_t)

## Reservoir Input
R_t = Reservoir(R_{t-1}, ε_t)

## Interpretation
- Reservoir encodes error dynamics
- WEMA performs controlled integration
- System minimizes prediction error over time
