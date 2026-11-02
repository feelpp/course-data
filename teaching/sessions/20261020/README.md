# 20 October 2026: covariance, Pearson and a first validation

Superseded by the [two-session multivariate route](../multivariate/README.md).
The earlier public page, slide attachments and interactive companion were removed
at the instructor's request. These authoring sources are retained for reference
and are no longer included in the website build.

Four hours including two ten-minute breaks. The audience is M1 CSMI. Python/pandas
basics, audit and univariate descriptions have been introduced; joint analysis
has not. The 25-minute recall is followed by covariance and a common-row matrix.
A 65-minute
block constructs standardisation and Pearson, including curvature, influential
observations and a 20-minute practical. The last block opens chronological
validation with a constant baseline; two ten-minute breaks are included.

At the instructor’s explicit request, class slides, the student sheet and the
five-page instructor guide are in French. The English reference site remains
unchanged. The instructor guide contains board calculations, timings, fallback
choices and Beijing reference results. It is kept outside the public website.

## Build

From the repository root, with its locked Python environment and Typst CLI
installed (verified with Typst 0.15.1):

```sh
uv run --with plotly==6.3.0 python teaching/sessions/20261020/build.py
```

The extra authoring package does not modify `pyproject.toml` or `uv.lock`.
The slides use Arial and Typst's bundled New Computer Modern Math and DejaVu Sans
Mono. On a machine without Arial, change the body font in `slides.typ` and `paper.typ`
to an installed font (`typst fonts`). All three PDFs use native mathematics;
no formula is rendered from a plain-text field in the lesson JSON.

Outputs are in `build/teaching/20261020/output/`:

- `pdf/20261020-covariance-pearson.pdf`: 37 native Typst slides: 35 for class
  and two optional complements.
- `pdf/20261020-student-exercises.pdf`: three pages with plotting skeletons and
  calculation tasks; no Beijing answers.
- `pdf/20261020-instructor-guide.pdf`: five teacher pages with answers.
- `20261020-interactive.html`: self-contained Plotly experiment, with no CDN.

Add `--publish` to update the student attachments used by the website. This copies
only the slides, student sheet and interactive companion. Rebuild Antora to see
them in the local website. The teacher guide is never copied to public attachments.
The exported Plotly HTML is versioned as `exports/interactive.zip`, a compressed
bundle containing the upstream Plotly JavaScript and our figure. Antora stages
its single HTML entry using only Python's standard library; site builds do not
need Typst or Plotly. The delivered HTML is still self-contained.

## Edit and execution model

- `slides.typ` is the canonical slide content, layout and native mathematical notation. Named
  Python raw blocks live directly in it. The local builder executes those trusted
  blocks in order, generates SVG figures and JSON calculations, then invokes Typst.
  Typst and the PDF viewer do not execute Python themselves.
- `../../slides/20261020-statistics.json` contains titles, timings,
  reference links and French facilitation notes. This is not an executable notebook.
- `exercises.typ` and `instructor.typ` contain the two handouts, using `paper.typ`
  for their shared style. `build_handouts.py` computes checked teacher references
  from the canonical local teaching CSV; none enter the student sheet or slides.
- Matplotlib figures are static vector assets in the PDF. Plotly interaction lives
  in the companion HTML. Keep the `pdf/` subfolder beside that HTML so the relative
  link in the worked Pearson slide works in PDF readers that permit local links.
- `build/teaching/20261020/manifest.json` records authoring versions and source hashes.

The notation is fixed: scalar covariance `s_xy`, matrix `S`, scalar Pearson `r_xy`,
correlation matrix `R`. Column means `m_j`, centred matrix `C` and standardised
matrix `Z` are defined before use. Mathematical indices start at one; NumPy
indices start at zero. The validation target count is `n_val`.

The optional matrix example connects centring to a Gram matrix; Pearson is a
cosine of
centred columns. These give CSMI students a bridge to projections, least squares
and later PCA without assuming joint analysis was already taught.

## Semester roadmap

`teaching/course-roadmap.json` adds mathematical tools and practical evidence to
the authoritative sequence in `curriculum.yml`. Its dated progress note records
introduced topics separately from planned block numbers.

```sh
uv run python tools/build_course_roadmap.py
uv run python tools/build_course_roadmap.py --check
```

This generates the SVG and expandable offline HTML linked from the course map.
It does not change the 28-hour curriculum or claim that a scheduled block is done.
