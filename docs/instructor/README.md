# Instructor workflow

## Canonical sources

English learning narratives, mathematics, worked examples, executable evidence,
and exercises are authored in AsciiDoc under `docs/course`. The Antora build
generates the corresponding solution-free notebook attachments; generated
notebooks are disposable and must not be edited by hand.

The sole notebook-native exception is
`notebooks/instructor/extensions/jax-transformations.ipynb`. Its Antora page is
authoritative for the English narrative, mathematics, environment boundary, and
transfer task. The notebook is authoritative only for the optional executable
JAX lab and student/instructor cell transformations.

## Notebook variants

Use these cell tags:

- `solution`: retained in the instructor variant and replaced by `metadata.course.student_source` in the student variant;
- `instructor-only`: retained only in the instructor variant;
- `remove-cell`: omitted from the student variant;
- ordinary cells: retained in both variants.

Generate both variants of the JAX exception with:

```sh
npm run notebooks:generate
```

Execute the fast reference set with:

```sh
npm run notebooks:test
```

The site build generates the AsciiDoc-first notebooks. Scheduled CI executes
the full reference set. Student notebooks are always output-free and have no
execution counts.

## Assessment boundary

The public repository may contain rubrics, specimen questions, and released assessments only after an explicit release decision. Live controls, final examinations, corrections, hidden tests, individual verification prompts, grading keys, and embargoed data stay in the private repository.

## Review checklist

- Verify importance and difficulty labels against `curriculum.yml`.
- Check that the stated time is realistic for an independent student.
- Restart and execute the reference notebook from a clean environment.
- Review plots, metrics, tolerances, and random seeds.
- Confirm data source, licence, checksum, schema, and attribution.
- Inspect the generated student notebook for leaked solutions.
- Build and visually inspect the Antora page and downloadable notebook.
