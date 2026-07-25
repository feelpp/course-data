# Technical release walkthrough — 2026-07-25

## Scope

This walkthrough checks the built artifact as a learner-facing technical
surface. It does not claim to be a representative-student, alumni, academic,
accessibility-specialist, or English-language review.

## Routes reviewed

| Learner task | Representative route | Technical expectation | Status |
|---|---|---|---|
| Orient in the course | course map and importance legend | P0--P3 meanings, prerequisites, duration, and assessment boundary are visible | Pass |
| Learn a mathematical method | stable linear and probabilistic models | inline/display mathematics, error estimation, insight callout, worked example, evidence, and conclusion render together | Pass |
| Reuse executable material | notebooks page and toolbar download | notebook is local, solution-free, English, and traceable to its AsciiDoc source | Pass |
| Understand assessment | assessment overview and public specimen | task IDs, points, importance, resources, AI mode, and rubric mappings agree with the generated notebook | Pass |
| Follow an optional route | JAX transformations | page/notebook authority and optional environment are explicit; required work has no JAX dependency | Pass |

The generated-site validator also traverses all local links and assets, checks
the main landmark, skip link, image alternatives, document language, local
notebook downloads, semantic worked-example sections, executable evidence, and
mathematics resources. The exact pinned KaTeX engine parses every inline and
displayed `stem` expression with error throwing enabled.

## Offline runtime

The rendered HTML has no third-party runtime script, stylesheet, image, audio,
video, source, or CSS URL. KaTeX JavaScript, styles, and fonts are copied into
the release; the UI's upstream web-font imports are replaced by its bundled
Roboto and Roboto Mono files; and UI icon definitions come from the local
bundle. External
citations remain ordinary links and do not block rendering or mathematical
reading when disconnected.

## Residual review work

The technical walkthrough cannot determine whether first-time CSMI students
understand the notation, whether the time estimates are realistic, whether a
screen-reader explanation is sufficient, or whether assessment wording is
unambiguous under timed conditions. The colleague pilot, two representative
students or alumni, named academic review, accessibility review, English
review, data-steward review, and assessment-custodian review therefore remain
pending and block any approved annual tag.
