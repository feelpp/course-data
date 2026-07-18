# Course decision record

**Course:** CSMI Data Processing and Mining  
**Decision date:** 2026-07-18  
**Baseline status:** approved  
**Supersedes:** recommendations in `docs/analysis/20260718_starter.md` where this record is more specific

## Settled decisions

### Language

- The entire public course site is in **English**.
- Navigation, Antora pages, notebook prose, exercise instructions, assessment briefs, rubrics, code comments written for students, figure labels, alt text, downloadable bundles, and repository contribution documentation are in English.
- French legacy material may be retained in the private/raw archive for provenance, but it is rewritten in English before publication. It is not exposed as a parallel French site.
- Technical terms follow standard international English usage. A glossary may explain synonyms, but the surrounding page remains English.
- Student submissions are expected in English. An instructor may approve an individual language accommodation without creating a second public course version.

### Course identity and workload

- Public title: **Data Processing and Mining**.
- Antora component/repository identifier: `course-data`.
- Programme position: CSMI M1, Semester 1.
- Credit/contact contract: 3 ECTS and 28 contact hours.
- Delivery baseline: fourteen two-hour blocks.
- The 28 hours include two in-class individual controls. Most mini-project work is outside contact hours; one two-hour clinic is included.
- The P0/P1 core is the binding 28-hour course. P2 content is optional or selectively project-assessed. P3 content is not required.

### Course boundary

- This course owns data provenance, quality, wrangling, EDA, leakage-safe pipelines, supervised baselines, statistical-learning fundamentals, PCA/clustering, evaluation, performance-aware local processing, and reproducibility.
- Project 1 owns Git/GitHub, CI/CD, containers, and project management as general skills; this course applies those skills to data artifacts.
- Database owns relational design, SQL, and NoSQL in depth; this course uses joins and analytical query interoperability without duplicating database theory.
- Random Models owns probability and stochastic processes in depth; this course uses probability to justify likelihood, losses, sampling, and uncertainty.
- Scientific Computing and Optimisation own numerical algorithms in depth; this course teaches the data-analysis consequences of conditioning, stable least squares, complexity, and gradient methods.
- Scientific Machine Learning 1 owns detailed JAX model construction, PyTrees, Optax training architectures, neural networks, accelerators, and physics-informed learning.
- One compact JAX/autodiff/JIT/vectorisation bridge may be offered as P2 after the P0/P1 core is secure.

### Priority and assessment policy

- `P0 — Essential`: taught explicitly, practised repeatedly, assessed individually, and eligible for the final exam.
- `P1 — Core`: taught and practised, assessed at least once, and eligible for announced assessments.
- `P2 — Extension`: optional/selected bridge or project material; never an unannounced prerequisite.
- `P3 — Deferred`: outside the 28-hour contract and transferred to another course or archive.
- Difficulty is separate: `D1 guided`, `D2 independent`, `D3 synthesis`.
- Every published learning artifact must declare concept ID, priority, difficulty, expected time, outcomes, prerequisites, and assessment status.

### Assessment model

- Control 1, individual practical: 20%.
- Pair mini-project plus individual verification: 25%.
- Control 2, individual audit/concept verification: 15%.
- Final individual practical/written exam: 40%.
- Continuous assessment therefore totals 60%. If programme regulations later require a different continuous/final ratio, task designs remain and only weights are amended explicitly.
- Current controls, exams, solutions, hidden tests, and grading scripts live in a separate private repository.
- Student work is collected through GitHub Classroom or an approved university platform, never a personal email account.
- Runtime-dependent grading uses fixed data/update budgets and tolerances, not wall-clock training competitions.

### AI-use policy

- The course implements the existing CSMI AI policy.
- Each assessment declares Mode A (external AI prohibited), Mode B (allowed with disclosure), or Mode C (AI collaboration is itself assessed).
- Ordinary exercises and the mini-project default to Mode B.
- In-class controls and the final exam default to Mode A unless the assessment header explicitly says otherwise.
- Mode B/C work includes an `ai-notes/` log and independent verification; confidential, personal, embargoed, hidden-test, and examination material must not be uploaded to external AI services.

### Publication and repository model

- Public repository: `course-data`, containing English notes, student notebooks, exercises, public tests, dataset snapshots/fetch recipes, rubrics, specimens, and released past assessments after embargo.
- Private repository: `course-data-assessment`, containing current assessments, variants, hidden tests, solutions, grading automation, and moderation records.
- A private branch in a public repository is not considered a security boundary.
- Antora is the publication backbone and `feelpp/antora-ui` is the UI.
- Production builds pin a reviewed UI release; the initial baseline is v0.53, subject to a tested upgrade during repository implementation.
- Antora/AsciiDoc is canonical for narrative and ordinary guided notebooks. Notebook-native/Jupytext sources are allowed only when rich notebook metadata requires them.
- Reusable logic lives in a Python package, not only in notebook state.

### Technical baseline

- Primary execution target: CPython 3.12 on Ubuntu 24.04 LTS, CPU-only.
- Supported student paths: native Linux, WSL2 with Ubuntu, and macOS.
- Python dependency/environment manager: `uv`, with committed `pyproject.toml` and `uv.lock`.
- Node dependencies are locked with `package-lock.json` and installed with `npm ci`.
- JAX is an optional dependency group; P0/P1 tasks do not require a GPU.
- Canonical student notebooks have outputs and execution counts stripped.
- Pull-request CI executes a fast CPU notebook subset; scheduled/release CI executes the full supported suite.

### Dataset decision

- Semester spine: UCI Beijing Multi-Site Air Quality dataset, snapshotted with checksums and attribution.
- Industrial classification case: UCI AI4I 2020 Predictive Maintenance dataset.
- Optional multiclass reserve: UCI Dry Bean dataset.
- Synthetic oracle datasets are generated from versioned code for conditioning, bias–variance, leakage, and metric tests.
- No class or assessment depends on a live download.
- Detailed rationale and licence records are in `datasets.md`.

## Accountable roles

Names can change without changing the governance model; every release must assign these roles in repository metadata.

| Role | Accountability |
|---|---|
| Course lead | Final academic scope, learning outcomes, assessment validity, release approval. |
| Content maintainer | English editorial consistency, Antora structure, notebook generation, issue triage. |
| Data steward | Dataset provenance, licences, checksums, schemas, datasheets, privacy review. |
| Assessment custodian | Private repository, variants, hidden tests, moderation, embargo and retention. |
| Technical reviewer | Environment locks, CI, CPU portability, security and reproducibility. |
| Academic moderator | Independent review of controls, final/retake equivalence, rubrics and accessibility. |

One person may hold multiple roles, but course lead and academic moderator must be distinct for high-stakes assessment review.

## Change control

A settled decision may change only through a pull request that includes:

1. a dated amendment below;
2. rationale and affected learning outcomes/assessments;
3. migration impact on published material and student commitments;
4. reviewer approval from the accountable role.

## Amendments

None.
