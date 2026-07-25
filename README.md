# CSMI Data Processing and Mining

This repository contains the English course site, executable labs, exercises, public tests, and licensed dataset snapshots for the CSMI M1 course **Data Processing and Mining**.

The site is built with Antora and `feelpp/antora-ui`. Course concepts are classified by importance from P0 Essential to P3 Deferred, and every published learning artifact declares its outcomes, priority, difficulty, duration, prerequisites, and assessment status.

## Quick start

Requirements:

- CPython 3.12;
- `uv`;
- Node.js 22 and npm 10 or newer.

Install and validate:

```sh
uv sync --locked --all-groups
npm ci
npm run check
```

Rebuild deterministic teaching tables or the single declared notebook-native source:

```sh
npm run data:build
npm run notebooks:source
```

Serve the generated site locally:

```sh
npm run serve
```

Then open `http://localhost:8087`.

Build and validate the deterministic solution-free student bundle:

```sh
npm run release:bundle
npm run release:check
```

Run one complete candidate preparation, including all 26 notebooks:

```sh
npm run release:prepare
```

Qualify a release by installing the locked required/optional environments, running
two clean preparations, and comparing the complete site, notebook, and bundle manifests:

```sh
npm run release:qualify
```

Candidate and annual tags remain subject to the human gates in `RELEASE.md`.

## Important paths

- `curriculum.yml`: learning outcomes, importance levels, concepts, schedule, datasets, and assessments.
- `docs/course`: Antora component and English course pages.
- `notebooks/instructor/extensions/jax-transformations.ipynb`: the only declared notebook-native exception; all other public notebooks are generated from English AsciiDoc pages.
- `build/notebooks/student`: generated output-free student notebooks.
- `datasets/snapshots`: checksum-pinned and attributed source datasets.
- `datasets/teaching`: deterministic classroom tables, manifests, and datasheets.
- `templates`: learning-delivery, pilot, feedback, assessment-statistics, retrospective, and approval starters.
- `tools`: generation and validation commands.
- `docs/governance`: course contract and settled decisions.
- `docs/analysis`: source audit and production roadmap.
- `build/release`: generated student bundle, checksums, and reproducibility report (ignored by Git).

## Publication boundary

The source archive and unresolved third-party material remain under ignored `archive/raw/` storage. Historical examinations and solutions belong only in the private `course-data-assessment` repository. The validation gate rejects raw archival content, solution trees, and roadmap sequence terminology outside the production roadmap.

## Licences

Original course prose, figures, and notebooks are licensed under CC BY 4.0. Repository software and automation are licensed under MIT. Dataset terms and attribution are recorded beside each snapshot. Raw archived sources are not covered by these licences.
