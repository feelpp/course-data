# Optional extension source and isolation contract

**Status:** accepted
**Effective date:** 2026-07-24
**Canonical inventory:** `curriculum.yml` → `enrichment_release`

## Purpose

Optional material should deepen the course without becoming a hidden prerequisite, an undeclared build dependency, or a second hand-maintained copy of eligible teaching content. This contract classifies every Extension (P2) page by source mode and records the permitted exceptions.

## Source modes

### AsciiDoc plus generated notebook

Use this mode when the page can teach the method, mathematics, executable evidence, interpretation, and exercises with the required CPU environment. The AsciiDoc page is canonical. Antora embeds selected results and `asciidoctor-jupyter` generates the cleared student notebook.

Every such extension must:

- declare `:page-jupyter: true`, `:page-course-execution-profile: full`, strict dynamic execution, and P2/not-assessed metadata;
- use no network, personal account, accelerator, or optional Python extra;
- contain deterministic, bounded evidence and visible interpretation;
- preserve valuable definitions, error estimates, assumptions, and mathematical insight on the webpage;
- remain absent from the required fast-notebook profile.

### Notebook-native exception

Use this mode only when a notebook carries behaviour that the shared AsciiDoc pipeline cannot safely represent or when executing it during the required site build would introduce an optional runtime. The notebook remains a reviewed canonical artifact, and its companion page explains the learning and environment contract.

“The notebook already exists” is not a valid reason.

### Page-only exception

Use this mode when execution would add no legitimate learning artifact, depends on a specialist environment, or would publish non-transferable evidence such as an undeclared machine benchmark. The page must still teach the method and state how a learner could gather valid evidence.

## Mandatory exception record

Every notebook-native or page-only exception in `curriculum.yml` has:

- a stable identifier;
- the page and, when applicable, notebook artifact;
- a specific reason;
- a named owner or owner relationship;
- the required environment;
- a maintenance policy and review trigger.

Repository validation rejects missing fields, duplicate identifiers, unclassified pages, overlapping classifications, missing artifacts, or an exception that silently enables Jupyter generation.

## Core-isolation rules

1. Extension pages have zero required contact hours and are not assessment eligible.
2. The required `fast` notebook profile contains only Essential/Core (P0/P1) CPU work.
3. Page-generated P2 notebooks use only required project dependencies and execute in the `full` profile.
4. JAX and Polars remain pinned only in the `extensions` extra.
5. P0/P1 pages and notebook sources may not import `jax` or `polars`.
6. The main Antora build does not execute or import notebook-native JAX or page-only Polars material.
7. Missing optional runtimes can fail the scheduled/release extension check, but cannot prevent completion of required notebooks or assessments.
8. No P2/P3 concept may appear as required assessment evidence.

## Learning-quality rules

An optional page is not a product brochure. Where mathematics gives useful insight, the page must present it next to the method and state both its consequence and its limit. Executable optional lessons use the same Context–Method–Implementation–Results–Conclusion reasoning chain as required worked examples, with Extension (P2) importance stated explicitly.

Results must distinguish:

- numerical correctness from statistical validity;
- validation evidence from untouched final evidence;
- distribution alerts from operational harm;
- machine-specific performance from algorithmic complexity;
- integrity checks from truth or authenticity.

## Current classification

| Page | Source mode | Rationale |
|---|---|---|
| Kernel methods | AsciiDoc plus generated notebook | Required NumPy/scikit-learn stack; deterministic CPU oracle |
| Probability calibration | AsciiDoc plus generated notebook | Required SciPy/scikit-learn stack; deterministic CPU oracle |
| Local experiment tracking | AsciiDoc plus generated notebook | Standard library and pandas; account-free local evidence |
| Drift and monitoring | AsciiDoc plus generated notebook | Required SciPy/scikit-learn stack; synthetic windows |
| JAX transformations | Notebook-native exception | Optional runtime and retained student/instructor cell transformation |
| Comparative dataframe engines | Page-only exception | Optional Polars and environment-specific benchmark evidence |
| Downstream CSMI paths | Page-only exception | Ownership map with no executable method |

The machine-readable form in `curriculum.yml` is authoritative.

## Review and retirement

Review an exception when its runtime, converter, assessment metadata, or owning course changes. Migrate it to AsciiDoc only when the page can remain the complete English learning source, the generated notebook retains necessary semantics, and the required build remains isolated.

Retiring an exception requires updating the curriculum classification, page, notebook index, validators, student bundle contract, review record, and this table in one change.
