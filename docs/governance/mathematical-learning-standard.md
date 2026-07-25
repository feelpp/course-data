# Mathematical learning standard

## Review finding

The first public implementation was strong as an executable laboratory and assessment contract but too terse as standalone teaching material. On 2026-07-18, all eight foundation pages and all seven analytical pages had zero AsciiDoc `stem` expressions; the analytical pages were only 29–33 lines. Students could discover what to do, but not reliably learn definitions, derivations, assumptions, or error estimation from the pages alone.

The reference style in the Feel++ Mathematics documentation uses explicit definition/theorem/example/exercise blocks, inline and displayed `stem`, and a progression from objects and assumptions to consequences and exercises. This course adopts that pedagogical structure while keeping its applied data-processing focus.

## Required structure for a mathematical method page

Every P1 method page must include:

1. notation and mathematical setting;
2. at least one explicit definition;
3. the objective, estimator, or transformation in displayed `stem` mathematics;
4. one derivation, proposition, or property with interpretation;
5. assumptions and identifiable failure modes;
6. an error-estimation section separating data, approximation, estimation, selection, and numerical errors as relevant;
7. one genuinely worked example whose inputs, intermediate calculations, executable evidence, and interpretation can be followed without hidden steps;
8. exercises requiring reasoning as well as implementation;
9. a link to an executable notebook that tests the mathematics.

Foundation pages containing sampling, metrics, optimisation, or numerical claims follow the same standard. Governance-only pages may remain primarily textual.

## Worked-example contract

A highlighted observation or one-line substitution is not a worked example. Every required P0/P1 worked example follows a visible learning sequence:

1. **Context:** state the stakeholder or research question, observational unit, units, data provenance, target quantity or decision, assumptions, and consequences of error.
2. **Method:** show the mathematical formulation, intermediate substitutions, baseline, validity conditions, and relevant error model. A visible *Mathematical insight* callout identifies any theorem, invariant, estimator property, conditioning result, or error relation that materially explains the example.
3. **Implementation:** reproduce the method from canonical data or a fully declared synthetic case using deterministic, commented code, assertions, declared inputs, and no hidden state. A page-only hand calculation uses a transparent semantic table rather than artificial code.
4. **Results:** present a bounded semantic table, scalar record, or question-driven accessible figure. State units, denominator, baseline or invariant, uncertainty or tolerance, and the exact claim supported by the evidence.
5. **Conclusion:** answer the context question before giving limitations. Distinguish observation, inference, prediction, and decision; name residual errors and the generalisation boundary.

Each part carries a visible importance meaning. Context, implementation safety, result reading, and conclusion are Essential (P0); the principal Master's-level method or theorem is normally Core (P1). Extensions do not interrupt the minimum reasoning path. A transfer task follows the solved example and changes one meaningful condition so students must reuse the method rather than copy its conclusion.

The executable evidence belongs with the solved example. A later laboratory is reserved for student work and must not be the first place where the page reveals the example's numbers, tables, or graphics. Code examples include comments that explain mathematical and data-processing decisions; comments do not merely narrate syntax. The complete authoring and review rules are in `docs/governance/worked-example-contract.md`.

## Rendering and accessibility

- Inline mathematics uses `stem:[...]`; displayed mathematics uses `[stem]` with `++++` delimiters.
- Every symbol is defined in prose near its first use.
- Equations are followed by interpretation; notation is not used as decoration.
- Tables and prose restate the operational meaning needed by screen-reader and non-specialist users.
- Colour is never the only carrier of mathematical meaning.
- Definitions, properties, examples, and exercises use named blocks and stable anchors.

## Error-estimation contract

Every empirical result distinguishes the target quantity from its estimate and reports relevant uncertainty. A complete error ledger considers measurement/data error, model approximation, finite-sample estimation, model-selection optimism, optimisation/numerical error, stochastic/Monte Carlo error, and population shift. Not every component can be assigned a valid confidence interval, but none should disappear merely because it is difficult to quantify.

## Automated review gates

Repository checks require every P0/P1 foundation or analytical page to contain exactly the ordered Context–Method–Implementation–Results–Conclusion structure, stable semantic IDs and roles, visible importance meanings, a checkable calculation, a Mathematical insight callout, a bounded result table, and a conclusion that names residual uncertainty or limitations. Notebook-backed pages keep executable evidence inside the example; every P1 method page includes both a result table and a diagnostic figure. Notebook checks preserve the same five headings and insight in the converted narrative. Generated-site checks verify the semantic sections, rendered insight, local KaTeX assets, output evidence, and page links.
