# Luna-71B-C4.2-I — P03 prediction semantics and lifecycle

**Status:** Documentary design; not adopted or implemented.  
**Disposition:** P03 representation is **RESOLVED BY DESIGN, conditionally**; source lifecycle evidence remains incomplete for completion predictions.  
**Authority:** Luna-71B-C4.2-I owner directions OD-I-1 through OD-I-4. No source changes or execution are authorized.

## Scope and exact source

This assessment inspects the H candidate source copies, not the published
checkpoint alone. The H worktree is branch
`governance/luna71b-c4-2-h-corrections`, HEAD
`e91818a5c974282e848dc43e52d3c0a534dcbf45`, tree
`f14f23f0eb00e8b4aa8946e34acc71ab46ab5749`. That Git tree does **not** identify
the uncommitted corrections. Candidate source copies and their full identities
are recorded in the H `gn/source-manifest.json` and
`gn/gn-artifact-manifest.json`; relevant H capture is additionally identified
by the I artifact manifest.

The cited source paths are:

* `gn/source/variants/{original,instrumented}/tpcn/predictive_coding.py`
* `gn/source/variants/{original,instrumented}/tpcn/luna70_readout_learning.py`
* `ppc11/capture.py` (H correction, not the model source)

Relevant source definitions are `Prediction`, `LocalPredictor.create_prediction`,
`expire`, `observe`, and `process_observation`; the two call sites in
`run_sequence_exposure`; the `observation_deadline` handler; and the readout
completion prediction creation path.

## Prediction-kind analysis

| Source prediction | Source-defined semantics | Expected symbol | Due / expiry | Source settlement path |
|---|---|---|---|---|
| `target_key="next_after_<symbol>"` | Created after the first A/B input. `predicted_value` is the source model's scalar `next_symbol_weights[first_symbol]`. It is compared against the second observation's numeric `SYMBOL_CODE`. | Not stored as a symbol field. The source later maps the same scalar to A/B using `A if predicted_value >= 0.0 else B` when constructing an omission signal. This is a candidate **DERIVED** value, not an observed field. | Both `expected_resolution_at` and `expires_at` are set to the common external deadline. | A second input becomes an observation and `LocalPredictor.observe` settles MATCHED. At a one-input deadline, the source creates a deadline-absence observation (`observed_value=0.0`) and settles the pending prediction through the same local path. `expire` settles EXPIRED only when `expires_at < observation timestamp`; it does not pre-empt the equal-time deadline observation. |
| `target_key="four_class_sequence_completion"` | Created after four readout activations; its scalar is `float(predicted_class)`. It is completion/readout bookkeeping, not an A/B symbol prediction. | **NOT APPLICABLE**. A class index must not be re-labelled as a symbol. | `expected_resolution_at=readout time + reward_delay`; `expires_at=readout time + 2*reward_delay`. | No corresponding observation or source settlement transition was found for this completion prediction. Do not infer settlement from classifier output, subsequent reward, or absence of later output. The missing path is a source behavior gap, not a successful terminal outcome. |

The symbol derivation is grounded in two exact source operations: the
`SYMBOL_CODE={"A": 1.0, "B": -1.0}` mapping used to encode the observed
symbol, and the existing omission conversion
`"A" if predicted_value >= 0.0 else "B"`. A proposed derivation may use only
the prediction's source scalar and this reviewed rule. It must not use labels,
evaluation payloads, filenames, class-specific branches, or output inferred
after settlement. The equality boundary at zero is explicitly A, not
unspecified.

Whether this conversion is accepted as the meaning of PPC-11
`expected_symbol` is an owner decision. Until accepted, it remains marked
DERIVED and cannot silently satisfy a source-observed requirement.

## Source-path-to-contract-field matrix

| Required P03 evidence | Source path / point | Proposed v2 field or record | Evidence status / limit |
|---|---|---|---|
| Prediction kind | Call site: next-symbol creation versus four-class completion creation | `prediction_kind` | `SOURCE_OBSERVED` from source call purpose/target key; exact enum and source locator retained. |
| Identity | `LocalPredictor.create_prediction` assigns `prediction_id` | `prediction_id`, `predictor_id` | Source-observed identity; no replacement ID. |
| Target | `Prediction.target_key` | `target_key` | Source-observed string. |
| Predicted value | `Prediction.predicted_value` | `predicted_value` typed `f64` | Source-observed exact bits; retain separately from symbol interpretation. |
| Expected symbol | No field on `Prediction`; source omission mapping converts the scalar | `expected_symbol_evidence` | `DERIVED` by the named, versioned rule for next-symbol kind; `NOT_APPLICABLE` for completion kind; `UNAVAILABLE` if the equation/input is not captured. |
| Creation time | `Prediction.created_at` | `created_at` | Source-observed exact source number. |
| Due time | `Prediction.expected_resolution_at` | `due_time` | Explicit `SOURCE_OBSERVED`, `NOT_APPLICABLE`, or `UNAVAILABLE`; no ambiguous null. |
| Expiry | `Prediction.expires_at`; `LocalPredictor.expire` | `expires_at`, `prediction_expire` | Capture on the actual expiration path. A null source value is encoded as typed `NOT_APPLICABLE`, not as missing evidence. |
| Observation identity/value | Event passed to `observe`; caller's symbol/event identity | `prediction_match.observation_event_id`, `observed_value`, and caller-supplied `observed_symbol` evidence | Source event/value observed; symbol may be source-derived from the known encoding and is marked DERIVED if not stored on the observation. |
| Match/settlement | `observe` selects prediction, removes it, increments matched count, emits `prediction_settle`; deadline caller emits match record | `prediction_match`, `prediction_settle` | Source-observed operation, disposition, time, event identity and lineage where available. |
| Expiry/settlement | `expire` removes records and emits expiration and EXPIRED settlement | `prediction_expire`, `prediction_settle` | Source-observed only when this method is reached. |
| Completion terminal state | No matching or completion settlement path found | `lifecycle_coverage` | `SOURCE_PATH_ABSENT`; not a settlement and not `COMPLETE_UNEXERCISED`. P03 remains incomplete for this lifecycle. |
| Capture failure | H capture callback raises or capture is unavailable | Out-of-band `capture_failure` | Must not be represented as source failure or successful settlement. |

## Required distinction among evidence states

Every conditionally applicable P03 field and transition must be represented by
one of:

* `SOURCE_OBSERVED`: read directly at the source operation.
* `DERIVED`: exact value and rule ID, with source input locators and equation
  identity.
* `NOT_APPLICABLE`: the prediction kind makes the field inapplicable.
* `UNAVAILABLE`: a value or transition should exist, but its evidence is
  missing; include a reason and source point.
* `COMPLETE_UNEXERCISED`: the source has a transition, and complete exposure
  evidence establishes that it did not occur. This is not appropriate for the
  completion prediction whose settlement path is absent.
* `SOURCE_PATH_ABSENT`: inspected source has no such model transition.

`null`, empty string, omitted field, and a successful terminal disposition
must not stand for these states.

## Proposed P03 representation

The detailed discriminated records and compatibility rules are in
[`04-proposed-versioned-trace-schema.md`](./04-proposed-versioned-trace-schema.md).
At minimum, v2 must preserve the scalar `predicted_value` and add a
schema-versioned `prediction_kind` plus explicit expected-symbol evidence.
The schema may identify the next-symbol symbol as DERIVED and the completion
symbol as NOT_APPLICABLE, but only after the owner expressly accepts that
contract revision. It must emit a separate `SOURCE_PATH_ABSENT` coverage
record for the completion settlement gap; it must not create a synthetic
settlement event.

## Conclusion

The proposed record model can distinguish symbol-bearing from
completion-oriented predictions without falsely stating that the model has a
symbol field or settlement transition it does not have. This resolves the
**representation design**, not the source evidence gap. `P03 capture` remains
**INCOMPLETE** until a separately authorized versioned contract is adopted
and the source capture is independently validated. No source or learning
behavior change is proposed here.
