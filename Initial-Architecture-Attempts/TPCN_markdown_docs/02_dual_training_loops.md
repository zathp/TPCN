# Dual Training Loops

## Genetic Loop (Slow)
- Learns priors, topology, and update rules
- Trained across many environments

## Environmental Loop (Fast)
- Local adaptation using prediction error
- Updates only local parameters

## Core Equation
theta_{t+1} = f_phi(theta_t, x_t, h_t, epsilon_t)
