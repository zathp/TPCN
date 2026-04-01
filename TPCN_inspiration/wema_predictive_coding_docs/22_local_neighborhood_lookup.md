# Local Neighborhood Lookup from Grid Points

## Overview

Once neurons are registered onto a grid, connection generation should happen by reading nearby grid points rather than searching the entire neuron population.

This gives each neuron a local field of view.

---

## Query Model

For neuron $i$ at position $p_i$:

1. compute its grid key $g_i$
2. enumerate nearby grid cells around $g_i$
3. collect neuron indices stored in those cells
4. filter by true geometric radius
5. generate or update weighted local connections

This separates:

- coarse filtering by grid cell
- precise filtering by Euclidean distance

---

## Nearby Cell Search

If the lookup radius is one cell in each direction, the queried stencil in 3D is:

$$
(2r_c + 1)^3
$$

cells, where $r_c$ is the search radius in cell units.

For $r_c = 1$, that is only 27 cells.

That is the key speedup: the number of checked cells is fixed even when the total neuron count grows.

---

## Local Connection Rule

After candidate neurons are collected, build edges only for truly local pairs.

Example weighting:

$$
w_{ij} = \max\left(0, 1 - \frac{\lVert p_i - p_j \rVert}{r}\right)
$$

where $r$ is the physical connection radius.

Optional modifiers can include:

- layer bias
- recent co-activation
- error-correlation strength
- maturity or openness gates

---

## Pseudocode

```python
def query_local_neurons(self, neuron_idx, search_radius_cells=1, connect_radius=None):
    neuron = self.neurons[neuron_idx]
    connect_radius = connect_radius or self.radius
    candidates = []

    for key in iter_neighbor_keys(neuron.grid_key, search_radius_cells):
        candidates.extend(self.grid.get(key, []))

    neighbors = []
    for other_idx in candidates:
        if other_idx == neuron_idx:
            continue
        other = self.neurons[other_idx]
        dist = np.linalg.norm(neuron.pos - other.pos)
        if dist <= connect_radius:
            weight = max(0.0, 1.0 - dist / connect_radius)
            neighbors.append((other_idx, weight))

    return neighbors
```

---

## Reading Grid Points

The phrase reading points on the grid can be treated as reading occupied spatial buckets.

Each neuron does not need direct awareness of every other neuron.
It only needs access to:

- the bucket it belongs to
- surrounding buckets within its search stencil

Those buckets act like local sensory points in the spatial fabric.

---

## Behavioral Consequences

This changes the reservoir in useful ways:

- connections emerge from physical locality
- clusters can form without explicit global sorting
- drifting neurons automatically discover new neighborhoods
- inserted neurons can connect immediately near their birth region

This is a better fit for a spatial predictive system than random global rewiring.

---

## Complexity Shift

Naive neighborhood build:

$$
O(N^2)
$$

Grid-based local lookup:

$$
O(N \cdot \bar{k})
$$

where $\bar{k}$ is the average number of local candidates per neuron.

If the grid is chosen well, $\bar{k}$ stays much smaller than $N$.

---

## Outcome

Grid-point lookup gives the reservoir a scalable local discovery mechanism.
The remaining requirement is to keep registration and connections correct while neurons are inserted, moved, and pruned over time.