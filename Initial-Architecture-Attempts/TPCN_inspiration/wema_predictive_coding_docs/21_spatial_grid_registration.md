# Spatial Grid Registration for Neurons

## Overview

The spatial reservoir should not discover neighbors by scanning every neuron.
Each neuron should instead register itself onto a spatial grid so that local queries only inspect nearby occupied cells.

This turns spatial topology from a global search problem into a local indexing problem.

---

## Core Idea

Each spatial neuron owns:

- a continuous position $p_i = (x_i, y_i, z_i)$
- a discrete grid coordinate $g_i = (u_i, v_i, w_i)$
- a cached list of nearby candidate neurons

The grid coordinate is computed from position and cell size:

$$
g_i = \left(\left\lfloor \frac{x_i}{h} \right\rfloor,
\left\lfloor \frac{y_i}{h} \right\rfloor,
\left\lfloor \frac{z_i}{h} \right\rfloor\right)
$$

where $h$ is the grid cell width.

---

## Registration Structure

Represent the grid as a sparse mapping:

```python
grid[(u, v, w)] -> [neuron_idx_1, neuron_idx_2, ...]
```

Only occupied cells need to exist.
This is important because the neuron field may be large while occupancy remains sparse.

Each neuron registers by:

1. computing its grid cell from its position
2. inserting its index into that cell bucket
3. storing the bucket key on the neuron for future updates

---

## Why This Matters

In the earlier spatial manager sketch, rebuilding neighborhoods compares each neuron with every other neuron.
That scales roughly like:

$$
O(N^2)
$$

For large open layers this becomes the wrong bottleneck.

With grid registration, a neuron only checks its own cell and adjacent cells.
If occupancy per cell stays bounded, expected lookup becomes closer to:

$$
O(k)
$$

where $k$ is the number of neurons in the local cell neighborhood, not the total neuron count.

---

## Spatial Interpretation

This matches the intended architecture from the Hmm notes:

- primitive neurons occupy constrained low-level regions
- anchor neurons form denser personal clusters
- open neurons spread through a larger exploratory space

The grid becomes the coarse scaffold that lets these regions discover each other efficiently.

---

## Registration API

Suggested neuron-side state:

```python
class SpatialNeuron:
    def __init__(self, idx, layer_type, pos):
        self.idx = idx
        self.layer_type = layer_type
        self.pos = pos
        self.grid_key = None
        self.neighbors = []
```

Suggested grid manager methods:

```python
register_neuron(neuron_idx)
unregister_neuron(neuron_idx)
move_neuron(neuron_idx, new_pos)
query_local_cells(grid_key, cell_radius=1)
query_local_neurons(pos, search_radius)
```

---

## Design Constraint

Cell width $h$ should be tied to connection radius $r$.

A practical rule is:

$$
h \approx r
$$

or slightly smaller.

That ensures a neuron can recover all possible local partners by searching a small fixed block of neighboring cells.

---

## Outcome

Grid registration provides:

- fast local candidate discovery
- a stable basis for neuron growth and drift
- incremental updates instead of full topology rebuilds
- a path toward GPU-friendly spatial bucketing

The next step is defining how neurons read from nearby grid points to generate local connections.