# TPCN Full System Specification

## Core Variables
x_t : input
h_i : neuron state
epsilon_i : prediction error
theta_i : fast weights
phi : genetic/meta parameters

## Predictive Coding
epsilon_i = x_i - x_hat_i

## State Update
h_i(t+1) = sum_k g_i^(k) * F_k(local_patch)

## Error Gating
epsilon_tilde_i = g_i^e * epsilon_i

## Learning Rule
Delta theta_i = f_phi(h_i, epsilon_tilde_i, neighbors)

All operations are local.
