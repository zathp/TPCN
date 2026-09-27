# Temporal Propagation Network (One-Step-Per-Neuron Concept)

## Concept

Instead of instantaneous forward propagation:

- Each neuron updates once per timestep
- Signals take time to propagate

## Rule

At time t:
- Layer 1 processes input
- Layer 2 processes previous state of Layer 1
- Layer 3 processes previous state of Layer 2

## This creates:

- implicit pipeline
- temporal depth instead of spatial depth

## Memory Role

Each neuron stores:
- its last activation
- incoming signals for next timestep

## Update Form

h_i(t) = f( inputs from neighbors at t-1 )

## Interpretation

- Network behaves like a dynamical system
- Depth emerges over time
- Similar to wave propagation
