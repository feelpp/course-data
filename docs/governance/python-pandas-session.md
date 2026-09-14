# Guided Python and pandas progression — 14 September 2026

The cohort cannot be assumed to know pandas. The first programming session now teaches a small set of table operations, with Python refreshed in context. Existing independent-level references remain available after guided instruction. The canonical schedule in `curriculum.yml` and the public course map retain fourteen two-hour blocks and 325 minutes of assigned preparation.

## Block 2: establish the basics

Use `foundations/python-pandas.adoc` and its generated notebook. Reuse the exact first-class table: A = 22 °C, B = 71.6 °F, C = 20 °C, D missing. The familiar question and hand calculation come before the code. No account, Git operation, database service, or prior pandas knowledge is needed for the lesson.

| Time | Facilitation | What students should explain |
|---|---|---|
| 0–20 | Open the notebook; revisit variables, lists, dictionaries, the conversion formula, imports, and errors. | Students identify a value, a key, a calculation, and its result. |
| 20–40 | Read the four-row CSV; distinguish Series, DataFrame, index, observation key, types, and units. | Students describe what one row means and read `(4, 3)`. |
| 40–65 | Predict then run selection, a mask, a derived column, and a missing-value check. | Students explain the selected rows and why missing is not zero. |
| 65–75 | Break. | Preserve the pause. |
| 75–105 | Finish the original mean together, then change one reading in a copy; swap predictor and typist. | A manual count and mean agree with code. |
| 105–120 | Explain assertions, synthetic provenance, and a limitation; restart the kernel. | Distinguish successful execution from understanding. |

Introduce one operation at a time. Ask for predictions before execution and let students describe the output before typing the next cell. Keep groupby, joins, reshape, broadcasting, and query optimisation out of this first session. The worked example is available on the webpage for students whose setup is blocked.

If the first selections remain unclear, use the pair-practice period for guided repetition. The core exit explanation is an explained selection, missing-value count, and mean. The function refresher can be revisited later; it is not an additional objective for this session. Do not accelerate through unread code to finish the page.

## Block 3: build on the same observations

Use `foundations/pandas-sql.adoc`. It keeps the first four readings and adds a second time for the same sensors. Allocate recap/grouping 20, guided join 25, break 10, quality decisions 20, pair practice 25, SQL demonstration 10, and explanation/checks 10 minutes. Count rows and available values separately. Name the change in unit after aggregation. Predict a many-to-one join, then check uniqueness, unmatched keys, and preservation. Distinguish missing measurements from missing metadata and unexpected values.

Introduce every technical word when first needed: a mask is a True/False choice per row; a join matches labels between two tables; a query is a request to a database. Prefer result, check, or explanation to evidence, and rules or requirements to contract unless a technical definition is necessary.

The SQL segment demonstrates an in-memory SQLite query whose result is a pandas DataFrame, with parity checked against a pandas selection. It establishes the Database course connection; schema design and performance are developed later. If the recap reveals persistent difficulty, use the demonstration slot for support and revisit the supplied SQL example in the Block 4 recap. Do not take time from the break or silently require extra preparation.

## Block 4 and later

Introduce shapes/column operations (10 minutes), long/wide reshape (10), and sampling (15); use the 55-minute EDA lab to practise the new representations on the teaching dataset, followed by uncertainty (20) and the checkpoint (10). The tabular reference includes bounded executable bridges before its full join example. Its complete reference route is not a pre-class assignment. Revisit arrays during the Block 6 methods introduction before least squares. Query-before-materialisation and performance remain in Block 12.

## Diagnostic and verification

The 35-minute readiness inventory records independent, with help, not yet encountered, or blocked. It has no entry pass/fail threshold. Paper table reasoning is separate from pandas exposure. Targeted support follows the guided sessions; a fresh-kernel environment run is required before independent notebook work, with supported participation while setup is blocked.

E01 is now the 25-minute paper audit, E02 the 55-minute first-table practice, E03 the 70-minute distributed grouping/join practice, and E04 the 55-minute EDA lab. E12 retains 65 minutes across the semester. Assessment weights and assessed outcomes remain unchanged; difficult independent tasks follow their guided preparation.

The two new lessons use the executable AsciiDoc contract: deterministic offline inputs, rendered results, notebook generation, clean execution, and source/notebook parity checks. Validate contact and preparation budgets and public-map parity. Automated success does not establish classroom timing: collect exit-ticket difficulties and revise pacing after teaching.
