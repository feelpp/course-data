# Release qualification

## Decision

The technical candidate has one declared source of truth for every public
learning artifact. The automated release gate installs locked dependencies,
builds the complete release twice from clean output directories, and requires
identical cryptographic inventories. This decision does not authorise a tag:
the representative-user pilot and named reviews remain pending.

## Source-of-truth inventory

| Artifact family | Authority | Generated public artifact | Editing rule |
|---|---|---|---|
| Foundation, analytical, assessment, and executable extension material | English AsciiDoc page under `docs/course/modules/ROOT/pages` | Antora HTML and solution-free `.ipynb` attachment | Edit the page; never edit generated notebooks. |
| Optional JAX laboratory | Split authority declared as `EXT-JAX-NB` in `curriculum.yml` | Antora page plus generated student/instructor notebook variants | Edit the page for narrative and mathematics; edit the notebook-native source only for executable JAX cells and transformations. |
| Non-executable references and ownership maps | English AsciiDoc page | Antora HTML | Keep page-only unless a real executable learning outcome is approved. |

The only notebook-native source is
`notebooks/instructor/extensions/jax-transformations.ipynb`. The retired
foundation and analytical notebook trees and their bespoke builders must remain
absent. Repository validation rejects an undeclared notebook-native source, and
student-bundle validation rejects any notebook outside the exact curriculum
inventory.

## Reproducibility gate

Run:

```sh
npm run release:qualify
```

The command installs the locked Python and Node environments, audits the Node
dependency boundary, and runs two complete clean preparations. It compares:

- every generated site path, size, and SHA-256;
- the complete tracked and untracked, non-ignored source-tree digest and whether
  the working tree is dirty;
- the site HTML and total file counts;
- the AsciiDoc-notebook manifest and notebook count;
- the student-bundle bytes, internal manifest, and file count;
- `uv.lock`, `package-lock.json`, the UI bundle, and both local Feel++ extension
  packages.

Success produces `build/release/reproducibility-report.json`. A mismatch is a
release blocker. The report deliberately preserves
`pending_pilot_and_named_signoff`; reproducible software is necessary but is
not academic, accessibility, language, data-steward, or assessment approval.
The site build also normalises Antora's wall-clock sitemap timestamps to
`SOURCE_DATE_EPOCH`; sitemap metadata therefore participates in the exact site
comparison rather than being excluded from it.

## Offline and language boundary

Rendered pages declare English at document level. Mathematics originates as
AsciiDoc `stem`; every expression is parsed by the repository-pinned KaTeX
engine during validation, and that runtime is copied into the
site. The build replaces the UI bundle's upstream web-font imports with its
bundled Roboto and Roboto Mono files. Icons use the local UI bundle. Site
validation rejects external runtime
scripts, stylesheets, media, CSS URLs, missing local assets, broken notebook
links, and non-English document declarations. Ordinary citations and links to
external evidence remain allowed because they are not required to render the
local lesson.

## Dependency and maintenance record

The release locks Antora, `asciidoctor-jupyter`, the local
`@feelpp/antora-extensions` and `@feelpp/asciidoctor-extensions` packages, the
Feel++ Antora UI bundle, KaTeX, and the Python environment. Any converter,
extension, UI, mathematics-runtime, or notebook-format update requires:

1. source/page/notebook contract tests;
2. execution of all 26 public notebooks in the full CPU profile;
3. student solution-leak and exact-inventory validation;
4. two clean release builds with an identical report;
5. visual inspection of representative mathematics, figures, tables, notebook
   downloads, navigation, and narrow layouts;
6. renewed human review where pedagogy, accessibility, wording, assessment, or
   data provenance could have changed.

The maintainer reviews dependency pins and the residual JAX exception at least
once per annual release. A new exception requires a curriculum record naming
its owner, environment, divided authority, parity contract, and removal
criteria.

## Approval status

Automated accessibility structure, English, mathematics, offline-runtime, and
technical walkthrough checks pass as technical evidence. The course lead must
not infer human approval from them. Academic moderation, independent
accessibility and English review, two representative students or alumni, data
steward review, and assessment-custodian review remain pending until named,
dated evidence is recorded outside the public repository.
