# CUDA Mapping Strategy

## Parallelization
Each voxel:
- independent WEMA update
- local reservoir state

## Kernel Layout
- thread per voxel
- shared memory for neighbor interactions

## Steps per Kernel
1. Load x_t
2. Update reservoir state
3. Compute α_t
4. Compute y_t
5. Store output

## Memory Layout
Use structure of arrays:
- x[]
- y[]
- α[]
- reservoir states[]

## Optimization
- coalesce memory access
- avoid branching
- fuse kernels where possible
