# WEMA Predictive Learning - Introduction

This document introduces using a Weighted Exponential Moving Average (WEMA) as a predictive model.

## Key Idea
Instead of smoothing a signal, WEMA is trained to predict the next timestep:
y_t ≈ x_{t+1}

This transforms WEMA into a learnable time-series model.
