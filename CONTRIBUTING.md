# Contributing

All public course content, code comments written for students, navigation, figures, alt text, exercises, and assessment specimens must be in English.

## Development workflow

1. Create a focused branch.
2. Update `curriculum.yml` if the change alters concept importance, outcomes, schedule, assessment coverage, or datasets.
3. Add or edit Antora pages under `docs/course/modules`.
4. Put executable examples in the AsciiDoc page so the site and notebook share one
   source. Edit `notebooks/instructor/extensions/jax-transformations.ipynb` only
   for the declared JAX notebook-native exception.
5. Run `npm run check` before opening a pull request.
6. Include the generated site artifact in review when layout or navigation changes.

## Required learning-artifact metadata

Every Antora page must declare:

```adoc
:page-course-language: en
:page-course-concepts: DP-...
:page-course-priority: P0
:page-course-difficulty: D1
:page-course-duration-minutes: 45
:page-course-outcomes: LO1
:page-course-prerequisites: None
:page-course-assessed: yes
```

AsciiDoc-generated notebook `metadata.course` carries the equivalent fields.
The JAX exception uses notebook cell transformations: a code cell tagged
`solution` must provide `metadata.course.student_source`, and cells tagged
`instructor-only` never enter the generated student notebook.

## Rights and provenance

Do not copy text, code, images, data, or examination content merely because it exists in the raw archive or on the web. Record the author, source, licence or written permission, and intended use. When rights are unclear, independently author a replacement.

## Public/private separation

Never add live examination prompts, hidden tests, solutions, grading keys, candidate data variants, or moderation notes to this repository. Those belong in `course-data-assessment`.
