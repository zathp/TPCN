# Dynamic Grid Growth and Connection Updates

## Overview

The grid index should support a living reservoir.
Neurons will be inserted, drift over time, and occasionally be pruned.
Connection discovery therefore needs to be incremental.

The correct approach is not to rebuild the full graph after every change.

---

## Incremental Update Rules

### 1. Insertion

When a new neuron is created:

1. choose a birth position
2. compute its grid key
3. register it in that cell
4. query nearby cells
5. establish local edges only to returned neurons

This keeps insertion cost local.

### 2. Drift

When a neuron moves:

1. compute the new grid key
2. if the key changed, remove it from the old bucket and insert into the new bucket
3. refresh only that neuron's neighborhood
4. optionally refresh neighbors that reference it

### 3. Pruning

When a neuron is removed:

1. remove it from its bucket
2. delete incoming and outgoing references
3. refresh local neighborhoods if needed

---

## Birth by Local Seeding

The Hmm blueprint already suggests inserting neurons near an existing region.
The grid design makes this explicit.

For a new neuron near parent set $S$:

$$
p_{new} = \frac{1}{|S|} \sum_{j \in S} p_j + \epsilon
$$

where $\epsilon$ is a small random offset.

After registration, the new neuron queries nearby cells and attaches locally.
This makes growth spatially coherent.

---

## Connection Cache Strategy

Each neuron may cache:

- current grid key
- current neighbor list
- last topology refresh step

This allows the system to avoid unnecessary lookup work every timestep.

A practical policy is:

- refresh immediately on insertion
- refresh on cell transition during drift
- refresh periodically every $T$ steps for stability

---

## Layer-Aware Lookup

Not every nearby neuron should be equally eligible.
Local search can still enforce architectural rules.

Example:

- primitive neurons mostly connect upward into anchor neurons
- anchor neurons maintain dense local recurrence and selective open-layer outputs
- open neurons connect broadly within local spatial neighborhoods

So the grid answers who is nearby, while the layer rules answer who may connect.

---

## Suggested Manager Extensions

```python
class SpatialGridManager:
    def __init__(self, cell_size, radius):
        self.cell_size = cell_size
        self.radius = radius
        self.neurons = []
        self.grid = {}

    def add_neuron(self, layer_type, pos):
        ...

    def move_neuron(self, neuron_idx, new_pos):
        ...

    def refresh_neighbors(self, neuron_idx):
        ...

    def refresh_local_region(self, grid_key, search_radius_cells=1):
        ...
```

---

## GPU Direction

This structure also prepares the system for accelerated implementations.

A future CUDA or torch implementation can store:

- neuron positions in dense tensors
- cell ids in integer tensors
- sorted neuron indices by cell id
- prefix ranges for each occupied cell

Then local lookup becomes a segmented neighborhood query rather than a Python object walk.

---

## Final Insight

The reservoir should grow by local registration, not global rediscovery.

That gives three important properties:

- scalable neighborhood search
- topology that stays tied to spatial meaning
- dynamic growth that remains computationally practical as neuron count increases

This is the right foundation if the open layer is expected to become large.