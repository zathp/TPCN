---
name: Luna-47E Hardware Realizability
description: Assess commercially obtainable FPAA and discrete/board-level realization of neuron primitives.
---

# Luna-47E — Bench-Buildable FPAA / Discrete Realizability

## Authorization and boundary

**AUTHORIZED / NOT EXECUTED.** This is analysis/evidence only. It does not
select or promote a production architecture, authorize a purchase or build,
or claim hardware equivalence. Do not assume custom ASICs, unavailable
research-only FPAA primitives, custom MEMS, unobtainable ideal
voltage-controlled resistors, or exotic memristors without a specifically
identified obtainable platform.

Source/evidence baseline: `2cef8ea4b37a4ae586e3f383511cba63c9268ddc`.
Use the common published Luna-0 authorization revision in
[`luna-0-authorization-luna47-20261006.md`](../../workflow/handoffs/luna-0-authorization-luna47-20261006.md),
a documentation-only descendant. Do not use unreviewed changes from other
lanes.

Read the architecture contract, changelog, workflow, acceptance criteria,
proposal process, handoff template, this contract and relevant retained
Luna-46 evidence. A15 is the primary boundary; A01-A04, A08 and A09 are
relevant implementation constraints. No clause change or ACP is proposed.

## Objective

For each primitive, map:

```text
ideal function -> commercially available FPAA implementation, if supported
               -> discrete / board-level fallback
```

At minimum evaluate:

- leaky integrator / WEMA and adjustable time constant;
- programmable resistance or conductance;
- capacitor implementation;
- comparator / deadband;
- rectification or absolute value;
- summation / subtraction and accumulation;
- threshold oscillator or equivalent bounded output mechanism;
- DAC / digital configuration interface.

Consider practical ordinary RC/op-amp circuits, digital potentiometers or
resistor banks, DAC-controlled biasing, comparators, and only verified FPAA
integrator/OTA resources on devices actually available for purchase. Varactors,
MEMS and other specialty approaches may be alternatives, not the baseline
without a clear prototyping advantage.

## Files and isolation

Own only `experiments/luna47e/`, `artifacts/luna47e/`,
`tests/test_luna47e_*.py` (if validation scripts are needed), and
`workflow/handoffs/luna-47e-hardware-realizability-20261006.md`.
Do not edit production/runtime code, other lane files, shared workflow or
architecture documents. Work from the common authorization revision.

## Required evidence and acceptance

For each candidate primitive give part/platform and manufacturer, precise
part number, function and limits, implementation notes, dated product-page
or distributor evidence, price/stock/lead-time if publicly shown, and source
URL plus retrieval date. Distinguish manufacturer capability from
independently verified present purchasability. Record the project owner's
confirmed region, supply/inventory constraints and budget only if supplied;
otherwise explicitly limit or mark owner-specific availability **BLOCKED**
rather than assuming access.

Include enough detail to judge whether a bench prototype is realistic:
power/voltage/current ranges, configuration path, time-constant/resolution
limits, component tolerances, board/package/accessories and known
implementation gaps. State assumptions and unavailable evidence. Provide a
machine-readable component/primitive matrix with source identities, revision,
configuration, fixture identities/hashes where used, and provenance. No
purchase or hardware experiment is part of this authorization.

## Exclusions and handoff

No product purchase, hardware build, circuit validation, equivalence claim,
architecture selection/promotion, or Luna-48 is authorized. Return a
completed handoff with findings, limitations and replayable/source-linked
artifacts; push the lane branch and stop for independent Luna-0 review.
