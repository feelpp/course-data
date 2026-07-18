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
7. one worked example with quantities that can be checked by hand;
8. exercises requiring reasoning as well as implementation;
9. a link to an executable notebook that tests the mathematics.

Foundation pages containing sampling, metrics, optimisation, or numerical claims follow the same standard. Governance-only pages may remain primarily textual.

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

Repository checks require each analytical page to contain structured mathematical blocks, displayed `stem`, error-estimation content, a worked example, and exercises. The mathematical-background page is part of the P0 foundation inventory. Generated-site checks continue to verify that MathJax assets and page links render successfully.
