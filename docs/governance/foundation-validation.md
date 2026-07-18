# P0 foundation-course validation

**Validation date:** 2026-07-18  
**Implementation status:** complete  
**Academic moderation status:** independent sign-off pending

## Delivered learning path

The P0 path now opens with a mathematical background chapter and covers the complete baseline workflow:

1. notation, norms, conditioning, probability, bias--variance, risk, sampling uncertainty, and the error ledger;
2. data lifecycle, question, provenance, and first audit;
3. NumPy/table semantics, tidy transformations, grouping, and validated joins;
4. schemas, types/units, missingness, duplicates, impossible values, anomalies, and data contracts;
5. EDA, sampling, representativeness, and truthful visualisation;
6. split/feature-time/selection boundaries, leakage-safe fitted pipelines, and dummy baselines;
7. regression/classification metric reasoning, thresholds, counts, and error analysis;
8. tests, datasheets, result cards, reproducibility manifests, and AI-assistance logs.

Nine English foundation chapters and seven foundation notebooks form the learning path. The notebooks are generated into clean student variants and execute in fast CPU CI. The final notebook is an integrated synthesis checkpoint that produces one traceable path from source/role audit through a protected pipeline, dummy comparison, metrics, errors, tests, and bounded result record. Every notebook declares concept IDs, importance, difficulty, duration, outcomes, prerequisites, assessment status, and execution profile. Solution and instructor-only cells are absent from student output.

## Data and templates

- UCI 501 teaching slice: 1,008 original hourly rows from three stations and fourteen March 2013 days, plus a source-file registry.
- UCI 601 teaching table: complete 10,000-row synthetic industrial classification case with target-derived failure fields explicitly excluded from predictors.
- Both teaching directories include source identity, CC BY 4.0, a datasheet, deterministic builder, row counts, sizes, and SHA-256 manifests.
- Public templates: dataset datasheet, result card, data contract, reproducibility manifest, and AI-assistance log.

## Automated evidence

`npm run check` passed after the mathematical-learning revision with:

- 13 repository/curriculum/notebook/data tests, including release-inventory and deterministic-cell-ID regression checks;
- 55-concept and 11-outcome curriculum validation;
- all 7 P0 notebooks executed on CPU;
- 7 solution-free student notebooks generated;
- 32 Antora HTML pages built;
- generated-site link, asset, inline/displayed mathematics, and MathJax checks passed;
- dataset snapshot and teaching-table checksums passed;
- public/private and naming-boundary checks passed.

Regenerating teaching tables and canonical foundation notebooks produces no content drift. The complete page, notebook, template, teaching-data, and specimen inventory is declared in `curriculum.yml`; validation rejects missing artifacts or a P0 notebook outside fast CI.

## Exit review

| Criterion | Status | Evidence |
|---|---|---|
| Student completes an end-to-end leakage-safe baseline from a clean clone | Pass | `baseline-synthesis.ipynb` integrates source/role audit, quality checks, split, fitted pipeline, dummy baseline, PR-AUC, error counts, result identity and limitations. |
| All P0 notebooks execute in CI | Pass | Seven notebooks selected by and completed in the fast profile. |
| Control 1 has a public specimen, point rubric, caps, private reference and hidden-test design | Pass | Public assessment pages and private specimen records. |
| Control 1 receives independent academic moderation | Pending external action | Private moderation checklist is ready; the academic moderator fields must be signed by a person distinct from the course lead. |

The remaining moderation item cannot be self-certified by the content author or an automated agent. No live Control 1 should be released until that sign-off and a timed student-level rehearsal are recorded.
