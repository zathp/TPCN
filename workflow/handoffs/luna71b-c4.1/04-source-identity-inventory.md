# Luna-71B-C4.1 Original/Instrumented Source Identity Inventory

**Purpose:** Record independently checkable source and artifact identities
available for documentary review. Hashes identify bytes; they do not prove
which bytes were loaded in historical execution or that the two implementations
behave equivalently.

## Repository and worktree identities

| Worktree | Branch | HEAD | Worktree observation |
|---|---|---|---|
| Active checkout | `feature/single-replay-3d-plasticity` | `54315aa8ac9340233c19d14f720eae771639fdea` | Clean before this C4.1 package was added |
| Original Luna-70 | `experiment/luna70-corrective-readout-learning` | `f117ce51e7a805564e37252d3b5c99bda163ce57` | Existing untracked Luna-70 files/artifacts preserved |
| Instrumented Luna-71B | `experiment/luna71b-instrumented-learning` | `f117ce51e7a805564e37252d3b5c99bda163ce57` | Existing untracked files/artifacts preserved |
| Prior C4 workspace | `experiment/luna71b-c4-bilateral-capture` | `f117ce51e7a805564e37252d3b5c99bda163ce57` | Existing untracked C4 artifact package read only |

## Original implementation and R6 evidence

Hashes were recalculated from the accessible original Luna-70 worktree. The
R6 files match the C3.1 and prior C4 records.

| File | Bytes | SHA-256 |
|---|---:|---|
| `tpcn/luna70_readout_learning.py` | 111,465 | `b2af493ad44ceca22a5d2994ebee53cb61cdc44d04ab743e34e7517d79f07b75` |
| `tpcn/luna66_minimal_learning.py` | 61,199 | `552b6a584ee540f69bc81ce92cffe6dd943ffca6e56ae74f6474f44bd314bb5f` |
| `run_luna70_corrective_readout.py` | 18,394 | `1d4ff78f184db7720b23795e6c16f30b6f88214979566c52baff4cb3d19da47f` |
| `tests/test_luna70_readout_learning.py` | 5,928 | `50ba3365ea60551d1354c4ee35e0eb006b7921d7a4458dc86fc67179700be262` |
| `artifacts/luna70/four-arm-results-r6.json` | 69,077,628 | `df54185fcbf02293c24589dbf1fd118c406e6651e1e4744a4ed0119f5715502d` |
| `artifacts/luna70/artifact-manifest.json` | 3,393 | `5a28e2950326ce2347760ee128effbd2b38208d5f477242208fb7537f74821fc` |

## Recovered source baseline and pilot preparation artifacts

All four source-baseline copies were located under
`TPCN-luna71b/artifacts/luna71b/source-baseline/` and independently hashed.
The two module copies are in `tpcn/`; the runner and test copies are at the
source-baseline directory root. All four match the corresponding original
Luna-70 source hashes above:

| Original/source-baseline pair | Bytes | SHA-256 | Comparison |
|---|---:|---|---|
| `tpcn/luna70_readout_learning.py` | 111,465 | `b2af493ad44ceca22a5d2994ebee53cb61cdc44d04ab743e34e7517d79f07b75` | Matches |
| `tpcn/luna66_minimal_learning.py` | 61,199 | `552b6a584ee540f69bc81ce92cffe6dd943ffca6e56ae74f6474f44bd314bb5f` | Matches |
| `run_luna70_corrective_readout.py` | 18,394 | `1d4ff78f184db7720b23795e6c16f30b6f88214979566c52baff4cb3d19da47f` | Matches |
| `tests/test_luna70_readout_learning.py` | 5,928 | `50ba3365ea60551d1354c4ee35e0eb006b7921d7a4458dc86fc67179700be262` | Matches |

| Pilot preparation evidence | Bytes | SHA-256 |
|---|---:|---|
| `artifacts/luna71b/L71B-C-paired-pilot-plan.json` | 133,178 | `60cde6b4929be4408fcecdcf3ac7104d5cb7b3365d94d55b568431e54fb5bc3f` |
| `scripts/prepare_luna71b_paired_pilot.py` | 22,629 | `9986a3cef2f2bb4776d9ecfb242f5998f301af809050e0040d1bc1a50d5021b9` |
| `artifacts/luna71b/L71B-C-preparation-execution.txt` | 9,275 | `f05033a8c78612610e8fdad1d6cd38b4541515a0ffdff7f4d5633301d6c8e7a6` |

## Instrumented implementation and shared runtime

Hashes were recalculated from the accessible Luna-71B worktree.

| File | Bytes | SHA-256 |
|---|---:|---|
| `tpcn/luna70_readout_learning.py` | 125,258 | `939b55ed6bfa27360e6be53122c91a26153b2b7531b9fb29ee0c4801e8bc2d55` |
| `tpcn/luna66_minimal_learning.py` | 61,199 | `552b6a584ee540f69bc81ce92cffe6dd943ffca6e56ae74f6474f44bd314bb5f` |
| `run_luna70_corrective_readout.py` | 26,126 | `f82eba8a5c5c0bed8b6aa7b51e9a83f2d3a920a8afbf15ec32f2bb859b7db7ac` |
| `tests/test_luna70_readout_learning.py` | 5,928 | `50ba3365ea60551d1354c4ee35e0eb006b7921d7a4458dc86fc67179700be262` |
| `tpcn/luna71b_trace.py` | 14,899 | `28b336061c029013545f1cf114e82ef60303f5ebc747fd92090e17aee1ded515` |
| `tpcn/event_runtime.py` | 10,558 | `151096ac3a1f6b1a528dfe9be98c8110385021bc453cdf9e5f0ad27e793ee77f` |
| `tpcn/canonical_neuron.py` | 6,905 | `f9878aad6da8ed507266e96d9e27eb09b29fcd4a1f96965f798a3b1520949595` |
| `tpcn/eligibility.py` | 9,899 | `6757e6a5886385b38f86989e050fb17b67b587a1fd7fe0a66e0ec2b85dd34814` |
| `tpcn/predictive_coding.py` | 10,838 | `5e0624fb1e3f53c6a4005ac9a893cbd4618d650ea7cd38950abda6de55252869` |
| `tpcn/topology.py` | 11,462 | `d5f1d6fc6911ed610e7fbff24c768551c00fb526a491f22cfae7d9e8ec1261fb` |

## Frozen fixture/selection identities

The hashed paired-pilot plan records these six full-split identities and
matches them to the R6 result (content / input-only). The C3.1 final review
reports spot-checking the six values in R6; it is not the source of the
individual digests:

| Split | Content SHA-256 | Input-only SHA-256 |
|---|---|---|
| Train | `888c60cfef2589de9a4d87bc07f1871d825cba15c3ae39ca9a7d5acba7e528bd` | `16e18d59096c2086d4cb421cc026105fac5705c325292b75d6aa752d443c55ce` |
| Validation | `0aa78955f44c55a066f0cb268990f50f39857511675caa8633f47749c8b0caff` | `459d4ec0c63ad20455446352c6e79f5c6405fd7442dd3c0d541b9ea59ca1c497` |
| Test | `5aee443c843e0a81bdfa60a12b50bac92a490dcab6dfea46b1874d26d49c33cf` | `2e999ef1582dabfaf5189ff8cf7814b90434ab66ab7a238ed7d34edf36ae8ef5` |

C3.1 corrects the pilot selected-generation and execution-order identities.
The complete values are available in the hashed paired-pilot plan:

| Split | Selected-generation content / input-only | Execution-order content / input-only |
|---|---|---|
| Train | `84d3c19fa668ae6a5902521f50cbed2b70171b4990e812836f4e8d96710f2002` / `075a34c6a97e8e664d4626e9fe2041ead0d014a6ba8cdc86b75d703f4e01c6c0` | `ca830710f6a7c9e87bd5ad62ca63baafe2a4cb4bc3ffa3f7093777a689719496` / `14fd313c3a4562abfb220316aaf81de9ad286a9469e1c90db3beeb1ba3af919c` |
| Validation | `10ae5da5624e97545bab4ae1659015f2b871e6c99be88c5763f9088b88fd50d1` / `0cc978f26051c671196186629b570c213df5c134b7f516c68230718ead9dc9a6` | Same as selected-generation |
| Test | `c0c17a48d5541ffb9911cd3dc086ee0497d967b19ee25a64ae2a0730b374152d` / `312f27b6c424c48ee401cf8c50d5a416e3aca9733bf4a21891064b0e116cc866` | Same as selected-generation |

These are different identity categories and must not be substituted for the
six full-split hashes. The selected-generation and execution-order pairs
above are read from the hashed paired-pilot plan and agree with the C3.1
correction. No dataset was regenerated in this work.

The R6 parameter digest is
`5a53d0cc7e41a7431d584bd711f0a1d0ba735a69f6e84b1b9298fa41f289948a`.
It is recorded as identical across all seeds; it is not a seed identity proof.

## Provenance limits

- The original and instrumented model file identities differ as expected;
  source identity alone establishes no parity.
- C3.1 says the original Luna-70 source files were byte-identical to recovered
  source-baseline copies. The current identity checks establish original and
  instrumented worktree file hashes; they do not independently bind historical
  R6 to loaded source bytes.
- The Luna-71A artifact package remains unavailable.
- Historical source-to-run lineage is not independently established.
- R6, source identities, and the reported split/parameter hashes do not prove
  any bilateral trace or execution result.
