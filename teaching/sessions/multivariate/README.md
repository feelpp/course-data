# Dated mathematical bridge: 20 October and 2 November

Authoritative notebook sources:

- `docs/course/modules/ROOT/pages/sessions/joint-variation.adoc`
- `docs/course/modules/ROOT/pages/sessions/matrix-geometry.adoc`
- `docs/course/modules/ROOT/pages/sessions/pca-practical.adoc`

These English AsciiDoc pages generate the notebooks with the repository's
vendored Antora/Jupyter converter. Do not maintain `.ipynb` sources here.
French oral supports are native Typst: `session-1.typ`, `session-2.typ`, and
`instructor.typ`, using the existing course typography. The small named Python
blocks in the decks execute before compilation and generate Matplotlib SVGs;
the PDF itself does not execute Python. The public lesson hub is
`session-multivariate.adoc`. The previous four-hour page and its public attachments
were removed; its authoring sources are retained outside the published site.

## Build and validate

Use the repository's locked Python environment, Node 22 and Typst 0.15.1.
NumPy, pandas, Matplotlib, nbclient and scikit-learn are already locked in
`pyproject.toml`/`uv.lock`; no additional presentation framework is introduced.

```sh
uv run python teaching/sessions/multivariate/build_seasonal_data.py
uv run python teaching/sessions/multivariate/build.py --publish
npm run site
npm run site:check
```

The first command verifies the pinned UCI snapshot checksum and extracts four
declared windows. It leaves the canonical March table unchanged. The second
executes slide figures, compiles both decks and instructor guide, checks exact
slide counts and dated timing metadata, generates all three notebooks with the Antora
converter, and executes every code cell in a fresh kernel. Failure aborts the
build. Student exercise comment skeletons are intentionally inert, not completed
answers. Publication requires successful notebook execution.

Outputs under `build/teaching/multivariate/`:

- `output/pdf/`: two dated decks and the instructor guide.
- `notebooks/`: deterministic, output-free generated notebooks.
- `executed/`: locally executed validation copies with figures.
- `validation.json`: source hashes, execution counts, tool version and computed
  PCA/regression reference values. A `--slides-only` run is a layout aid, not
  complete notebook validation.

`--publish` copies the two student PDFs into Antora attachments; the instructor
guide remains a local instructor artifact. Antora generates public notebooks,
renders code/results with the existing dynamic-block processor and includes
the prepared datasets in the offline student bundle. Closed code panels contain
independently closed Results panels. Propositions remain visible, with short
proofs in standard `%collapsible` blocks; proof content survives notebook conversion.

## Teaching choices

20 October: the instructor reports a four-hour class ending at the Pearson
matrix. The first deck and page group the paired analysis and the first three
matrix sections of the former second session. The timing mode is `record`:
no fabricated retrospective minute-by-minute schedule. The existing 5 October
practical was assigned for completion, not declared completed by every student.

2 November: a planned 120-minute session, with the transition from S/R to new
coordinates, the maximum-variance argument, SVD and a 45-minute guided PCA
practical. The timetable reserves minutes 60–105 for the practical. Students
can center and multiply matrices but need time; optional hints and three
checkpoints support those calculations. The common experiment compares two
and three components, while unit/variable changes remain extensions. The independent student practical has
provided data loading and plotting scaffolds, but leaves PCA computations and
interpretations to students. Comment scaffolds execute without producing
answers; zero generated figures are therefore expected for this notebook.
The lesson notebook retains complete worked demonstrations as a reference.

Regression begins on 9 November (planned) toward supervised learning. The
closing five minutes on 2 November only pose the response-estimation question;
no fitted line is required.
Full least-squares proofs and the chronological Beijing experiment are clearly
marked as reference/preparation, not required work in the November 2 PCA TP.
The 14-block, 28-hour semester contract remains unchanged; the dated route
records six existing contact hours, rather than adding sessions to that plan.

Notation: population `X,Y,mu,sigma,rho`; observed `x,y,s,r`; data matrix
`A`, centered `A_c`, sample covariance `S`, diagonal **variances** `D`, standardized
`A_z`, correlation `R`; principal directions `v_j`, scores `z_j`; bold `X` for
the regression design. Economy SVD uses `q=min(n,p)` and allows zero singular
values; restricted conditioning refers only to the nonzero singular subspace.

The regression task estimates same-hour PM2.5 from available same-hour sensors.
It does not forecast unknown future covariates. Train-only transformations and
timestamp separation prevent mechanical preprocessing leakage, but the already
explored teaching slice is not an independent final benchmark. Hourly and
cross-station dependence are stated throughout.

The opening of Session 1 recalls the probability space, random versus observed
quantities, expectation/covariance rules and i.i.d. pairs before the plots.
Two slides detail why independence factorizes the expectation of a product
and makes covariance zero. The opening web recap includes the corresponding
collapsible proof and an independent-coin example, retained in the notebook.
Use `Q_XY` for the random centered-product sum and `q_xy` for its realization;
`S_XY` is the estimator and `s_xy` its observed value. Population covariance
is `sigma_XY`. The main slides show the core proof; four-term algebra, the
centering rank/trace proof and Monte Carlo comparisons at n=5,20,100 are
notebook/reference material. The matrix material is now part of the dated October page. November begins
with a short recall and does not assume PCA or regression was already taught.
