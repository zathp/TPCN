# CUDA Implementation Sketch

Per voxel thread:
1. Load local patch (shared memory)
2. Compute 10 pathways
3. Compute gates
4. Combine outputs
5. Apply gated delayed error

Maps well to stencil computation and GPU parallelism.
