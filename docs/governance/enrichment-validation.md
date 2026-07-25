# Optional enrichment validation

**Validation date:** 2026-07-24
**Implementation status:** complete
**Assessment status:** excluded
**Canonical inventory:** `curriculum.yml` → `enrichment_release`

## Delivered source modes

| Route | Importance | Source mode | Evidence boundary |
|---|---|---|---|
| Kernel methods | P2 Extension | English AsciiDoc plus generated notebook | CPU oracle, spectral stability, held-out comparison; no large-\(n\) claim |
| Probability calibration | P2 Extension | English AsciiDoc plus generated notebook | Proper scores, reliability uncertainty, leakage-safe calibration |
| Local experiment tracking | P2 Extension | English AsciiDoc plus generated notebook | Account-free local records; no truth/authenticity claim |
| Drift and monitoring | P2 Extension | English AsciiDoc plus generated notebook | Marginal and conditional evidence separated; no automatic retraining |
| JAX transformations | P2 Extension | Documented notebook-native exception | Optional CPU runtime; no PyTrees, Optax, neural networks, or accelerators |
| pandas/DuckDB/Polars comparison | P2 Extension | Documented page-only exception | Protocol and lower bounds; no portable timing claim |
| Downstream course map | P2/P3 boundary | Documented page-only exception | Ownership map; no artificial executable artifact |

The detailed eligibility and exception rules are in `docs/governance/optional-extension-contract.md`. Findings for every page are in `docs/reviews/20260724_optional-extension-review.md`.

## Web learning and mathematics

The four AsciiDoc-generated lessons are complete webpage learning resources rather than notebook launchers. Each presents definitions, assumptions, error estimation, a prioritised mathematical insight, an ordered worked example, executable evidence, interpretation, limitations, and exercises.

Important mathematics now includes:

- Gram-matrix positive semidefiniteness, spectral regularisation, perturbation bounds, and dense complexity;
- calibration as a conditional expectation, proper scores, reliability-bin uncertainty, and monotone ranking invariance;
- marginal versus conditional drift, KS distance, standardised shifts, and multiple-testing bounds;
- canonical run identity, checksum limits, and validation-selection bias;
- JAX central-difference error and scale-aware gradient discrepancies;
- I/O and raw-memory lower bounds for dataframe engines.

## Core isolation

The enrichment inventory declares zero required contact hours, no assessed concepts, and a separate dependency extra. Foundation and analytical inventories contain no extension path. Required P0/P1 pages and notebooks do not import JAX or Polars.

The normal locked environment contains everything needed to build the four AsciiDoc-generated optional pages, but those notebooks carry the `full` profile and are absent from required fast-notebook completion. The Antora build does not execute the notebook-native JAX notebook or a Polars benchmark.

The scheduled/release full-notebook workflow installs the `extensions` extra and executes JAX on CPU. Removing the seven extension pages, five optional notebooks, builder, and dependency extra leaves the complete 28-hour schedule, four assessments, all P0/P1 concepts, and seventeen core lesson notebooks intact.

## Exception validation

Every exception has a stable ID, reason, owner, environment, and maintenance policy in `curriculum.yml`, with the same information visible on its page. Repository validation rejects:

- an enrichment page outside P2 or marked assessed;
- an unclassified or multiply classified page;
- a generated-page source without strict/full Jupyter metadata;
- a missing exception field or artifact;
- optional imports in P0/P1 sources;
- optional pins outside the declared `extensions` extra;
- a P2/P3 assessment mapping.

## Automated gates

The required profile validates the CPU-only core without importing optional runtimes. The full profile executes the four AsciiDoc-generated extension notebooks and the notebook-native JAX artifact when the optional environment is installed. Site validation checks the generated extension notebooks, manifest inventory, rendered STEM, semantic tables, figures, accessibility text, and source-specific learning terms.

Generated student notebooks are cleared and solution-free. Release-bundle validation requires all five optional notebook artifacts while its start instructions continue to distinguish the required environment from the optional JAX runtime.

## Remaining human gates

Technical implementation does not authorise release. Named instructor mathematical review, downstream-owner review, representative-student webpage review, and accessibility sign-off remain pending under the existing annual release procedure.
