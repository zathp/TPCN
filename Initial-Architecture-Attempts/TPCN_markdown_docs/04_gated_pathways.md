# 10 Gated Pathways

Each neuron computes 10 local transformations:

h_i_new = sum_k g_i^(k) * h_i^(k)

Where:
- g_i^(k) are learned gates
- Each pathway specializes (prediction, filtering, memory, etc.)

Encourages competition and specialization.
