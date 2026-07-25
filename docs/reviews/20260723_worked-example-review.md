# Worked-example consistency review

Date: 2026-07-23

Scope: 12 foundation and seven analytical lesson pages

Technical status: implemented; complete automated verification passed

Human status: instructor and real-student webpage review pending

## Review outcome

All 19 canonical worked examples now use the same visible learning chain:

`Context → Method → Implementation → Results → Conclusion`

Every part displays its importance, and every Method section contains a rendered Mathematical insight callout. The callouts retain mathematics that changes how a student should select, implement, diagnose, or interpret a method. They also state the limit of the insight, so the page does not present a theorem or formula as a universal guarantee.

The migration preserved existing datasets and computations. It separated the reasoning stages, strengthened page-level conclusions, and made valuable mathematical content visible without moving it into notebook-only commentary.

## Inventory and mathematical findings

| Lesson | Delivery | Important mathematical insight now made explicit | Importance | Evidence |
|---|---|---|---|---|
| Mathematical background | page | stem:[\operatorname{Var}(\bar X)=\sigma^2/n] under independence distinguishes row spread from uncertainty of the mean; covariance can break the square-root law | Essential (P0) | hand calculation and semantic table |
| Probability distributions and moments | page + notebook | the Poisson model implies equality of mean and variance, making the dispersion ratio a falsifiable moment diagnostic | Core (P1) | hand ratio and generated table |
| Quantiles, exceedance, and risk | page + notebook | a predeclared exceedance indicator converts tail-risk estimation into Bernoulli mean estimation with stem:[p(1-p)/n] variance | Core (P1) | interval calculation and generated table |
| Mean and uncertainty | page + notebook | Studentisation accounts for estimation of scale; the stem:[t] theorem does not repair dependence, bias, or population mismatch | Core (P1) | hand interval and generated table |
| Data lifecycle | page + notebook | the estimand determines weights, so row-weighted and equal-station means are different questions rather than numerical disagreement | Essential (P0) | two estimates, figure, and audit |
| Tabular data and joins | page + notebook | many-to-one join cardinality is a conservation law for the observation key and row count | Essential (P0) | generated join table and assertions |
| Data quality | page + notebook | quality rules written as indicators produce reproducible counts; using the same predicate is required for valid before/after comparison | Essential (P0) | generated audit table |
| EDA and sampling | page + notebook | aggregation changes the unit and weighting; missing hourly coverage affects both uncertainty and the implicit estimand | Essential (P0) | summary table and time figure |
| Safe pipelines | page + notebook | leakage changes the information set and therefore the predictive problem; resampling cannot repair a violated feature-time boundary | Essential (P0) | protected baseline table and assertions |
| Metrics and errors | page + notebook | a threshold plus costs and a population defines empirical decision risk; selecting it on protected data creates optimism | Core (P1) | threshold consequence table |
| Reproducible delivery | page | absolute and relative tolerances encode scale and conditioning; an unjustified tolerance can conceal forward error | Essential (P0) | hand bounds and decision table |
| Baseline synthesis | page + notebook | constant-score average precision equals evaluated prevalence, providing the correct ranking baseline but not calibration or a threshold | Core (P1) | end-to-end evidence record |
| Linear and probabilistic models | page + notebook | small singular values amplify perturbations and normal equations square the condition number | Core (P1) | exact fit, solver table, and singular-value figure |
| Classification losses | page + notebook | log loss is strictly proper and evaluates probability information discarded by a hard threshold; `logsumexp` preserves the objective numerically | Core (P1) | hand loss, stability table, and loss figure |
| Regularisation and generalisation | page + notebook | Ridge spectral shrinkage trades bias for variance and changes the estimator; Lasso zeros are not causal proof | Core (P1) | orthogonal calculation, protected table, and coefficient figure |
| Model selection | page + notebook | the resampling unit defines target risk; repeated rows do not create independent deployment units | Core (P1) | fold table and paired diagnostic figure |
| Trees and ensembles | page + notebook | Gini gain is local empirical optimisation; bagging variance reduction and boosting correction do not replace protected evaluation | Core (P1) | hand gain, model table, and PR-AUC figure |
| PCA and clustering | page + notebook | PCA's theorem minimises squared reconstruction error, not loss of scientific relevance or cluster truth | Core (P1) | eigenvalue calculation, validation table, and score plot |
| Columnar performance | page + notebook | raw payload is a lower bound on peak memory; projection and pushdown remove terms before materialisation | Core (P1) | memory calculation, equality table, and storage figure |

## Consistency checks

- Exactly one canonical worked example exists on each inventoried page.
- The five level-three headings occur once and in the required order.
- Stable IDs and semantic roles identify every part.
- Context, Implementation, Results, and Conclusion are visibly Essential (P0).
- The Method is visibly Essential (P0) or Core (P1).
- All 19 Method sections contain a Mathematical insight callout.
- The two page-only examples use transparent calculations rather than unnecessary Python.
- The 17 notebook-backed examples retain deterministic executable evidence.
- Results distinguish tables, scalar evidence, or justified figures according to the question.
- Conclusions answer the question and name residual error or limitations.

## Automated and rendered evidence

The final verification completed on 2026-07-23:

- Ruff lint and formatting checks passed;
- 24 Python tests passed;
- both AsciiDoc conversion and execution contract suites passed;
- repository validation passed for 55 concepts and 11 outcomes;
- all 14 fast notebooks executed successfully;
- all 22 full-profile notebooks executed successfully;
- generated-site validation passed for 49 HTML pages;
- all 17 worked-example notebooks preserved the five headings, visible importance, Mathematical insight, code order, and cleared student outputs;
- all 19 rendered pages preserved their semantic roles, stable IDs, titled Mathematical insight, tables or figures, STEM, and accessibility contracts;
- the 98-file student bundle was rebuilt and passed privacy, output-state, manifest, and checksum validation.

Representative browser review covered:

- the analytical linear/probabilistic example, including SVD conditioning mathematics, semantic section navigation, generated table, and diagnostic figure;
- the executable data-lifecycle foundation example, including the estimand insight, two result tables, and figure;
- the page-only mathematical-background example, including the standard-error theorem, hand calculation, and static semantic table.

`asciidoctor-jupyter` preserves the admonition body but drops its custom title. The source therefore includes a notebook-portable `Mathematical insight` label inside the admonition. Course CSS hides only that fallback label on the webpage, where the richer titled admonition remains visible. Automated checks require both representations.

## Remaining human gates

Technical completion does not claim that students have validated the pages. Before release:

1. a named instructor reviews every mathematical statement, unit, assumption, error claim, and conclusion;
2. an accessibility reviewer checks the rendered insight blocks, STEM, tables, and figures;
3. representative students use selected foundation and analytical webpages without instructor prompting and identify the context, method, insight, implementation, result, dominant error, and conclusion;
4. findings and required corrections are recorded here or in a dated follow-up review.
