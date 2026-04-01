# Core Equations

## Pathways
h_i^(k) = F_k(N_i)

## Gating
g_i^(k) = sigmoid(G_phi(h_i, epsilon_i, N_i))

Constraint:
sum_k g_i^(k) <= 1

## Combined Output
h_i = sum_k g_i^(k) * h_i^(k)

## Delayed Error
epsilon_i(t) -> buffer -> epsilon_i(t - tau)

## Update Rule
theta_i(t+1) = theta_i(t) + f_phi(h_i, epsilon_i, neighbors)
