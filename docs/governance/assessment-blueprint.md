# Assessment blueprint

**Baseline:** 60% continuous assessment, 40% final exam  
**Contact-time assumption:** Control 1 and Control 2 occur inside the 28 hours  
**Assessment language:** English  
**Operational rule:** current assessments and solutions remain in `course-data-assessment`, a separate private repository

## Design principles

Assessments measure the complete evidence chain:

1. Is the question and unit of analysis correct?
2. Are the data traceable, lawful to use, and validated?
3. Are transformations and joins correct?
4. Is evaluation protected from leakage?
5. Is the method justified by assumptions and baselines?
6. Are metrics, uncertainty, failures, and limitations interpreted?
7. Can the result be reproduced and tested?

No assessment awards most marks solely for model accuracy. P0 failures may cap the affected criterion even when final metrics look good.

## Outcome coverage matrix

Legend: `I` individual direct evidence, `T` team evidence, `V` individual verification, `—` not a primary target.

| Learning outcome | Control 1 | Mini-project | Control 2 | Final |
|---|:---:|:---:|:---:|:---:|
| LO1 Problem/unit/stakeholders | I | T+V | I | I |
| LO2 Provenance, privacy, schema, quality | I | T+V | I | I |
| LO3 Wrangling and validated joins | I | T+V | I | I |
| LO4 EDA and visual communication | — | T+V | I | I |
| LO5 Leakage-safe pipelines | I | T+V | I | I |
| LO6 Splits, baselines, metrics, failures | I | T+V | I | I |
| LO7 Statistical learning and mining methods | — | T+V | I | I |
| LO8 Computational/memory/storage reasoning | — | T+V | I | I |
| LO9 Tests and clean rerun | I | T+V | I | I |
| LO10 Datasheet, result card, limitations, AI log | — | T+V | I | I |
| LO11 SciML/HPC bridge | — | optional | — | — |

LO11 is a P2 bridge and is deliberately excluded from required individual assessment.

## Control 1 — data audit and safe baseline

- Weight: 20%
- Duration: 70 minutes
- Work mode: individual
- AI mode: A
- Environment: provided CPU environment; offline dataset snapshot
- Position: after Block 8, with content limited to announced P0/P1 topics

### Candidate task

Students receive two related tables with deliberate but realistic issues. They must:

1. state the unit of analysis and expected join cardinality;
2. validate the join and demonstrate that rows were neither silently duplicated nor lost;
3. identify and handle type/unit, missing, duplicate, and range problems;
4. write at least two executable data-quality checks;
5. create an appropriate split before learned preprocessing;
6. construct a numeric/categorical baseline pipeline;
7. choose and interpret one metric and one failure mode;
8. provide a one-paragraph limitations note.

### Scoring

| Criterion | Points |
|---|---:|
| Unit of analysis and join validation | 4 |
| Data-quality diagnosis and justified handling | 4 |
| Executable checks/tests | 3 |
| Leakage-safe split and preprocessing pipeline | 5 |
| Baseline, metric, interpretation, limitations | 4 |
| **Total** | **20** |

Critical cap: fitting preprocessing on the test set or using target-derived information in features limits the pipeline criterion to 1/5 unless the student identifies and corrects the error.

## Mini-project — reproducible scientific/industrial analysis

- Weight: 25%
- Work mode: pairs, plus individual verification
- AI mode: B
- Contact support: Block 13 clinic
- Submission: private GitHub Classroom repository and tagged release

### Required repository artifacts

- `README.md` with question, run commands, and repository map;
- `pyproject.toml` and lock file;
- data registry entry, checksum, attribution, licence, and datasheet;
- reusable functions under `src/` where appropriate;
- notebook/report with baseline, validation, results, uncertainty, error/failure analysis, and limitations;
- public tests and passing CI;
- concise result/model card;
- `ai-notes/` log or explicit declaration that no AI assistance was used;
- release artifact generated from the assessed commit.

### Pair rubric

| Criterion | Points |
|---|---:|
| Question, scope, unit, stakeholders, success criteria | 2 |
| Data provenance, licence, datasheet, privacy/ethics | 3 |
| Quality checks, transformations, joins, EDA | 4 |
| Leakage-safe pipeline, baselines, method justification | 4 |
| Evaluation, uncertainty, failure analysis, limitations | 4 |
| Tests, CI, environment, clean rerun | 4 |
| Technical communication and result card | 2 |
| **Pair subtotal** | **23** |

### Individual verification

Each student receives 5–8 minutes to explain or modify a selected part of the repository. The individual verification contributes 2 points and can trigger an individual adjustment when authorship or understanding differs materially within the pair.

## Control 2 — audit a flawed analysis

- Weight: 15%
- Duration: 45–60 minutes
- Work mode: individual
- AI mode: A
- Position: Block 14

Students inspect a short analysis containing a controlled selection of defects, such as:

- many-to-many join amplification;
- target or temporal leakage;
- global imputation/scaling before cross-validation;
- inappropriate metric under imbalance;
- tuning on the final test set;
- causal interpretation of predictive association;
- missing licence/provenance;
- irreproducible random state or hidden notebook state;
- unsupported performance claim without uncertainty;
- personal/confidential data passed to an external service.

### Scoring

| Criterion | Points |
|---|---:|
| Defect identification | 5 |
| Explanation of consequence | 4 |
| Correct repair | 4 |
| Prioritisation and concise communication | 2 |
| **Total** | **15** |

## Final exam

- Weight: 40%
- Duration: 2 hours 45 minutes
- Work mode: individual
- AI mode: A by default
- Environment: self-contained, CPU-only, offline-capable
- Data: unseen context, familiar data types and task structure

### Blueprint

| Section | Share of exam | Evidence |
|---|---:|---|
| A. Data audit and pipeline repair | 25% | Schema, joins, missingness/anomalies, leakage. |
| B. Mathematical and method reasoning | 25% | Likelihood/loss, regularisation/bias–variance, trees or PCA/clustering. |
| C. Implementation and tests | 25% | Small correct transformation/model/metric and toy-oracle tests. |
| D. Evaluation and interpretation | 15% | Metric choice, uncertainty, failures, limitations. |
| E. Reproducibility and governance | 10% | Provenance/licence/privacy, run manifest, AI mode. |

### Construction constraints

- Use fixed iteration/epoch/update counts and deterministic seeds where possible.
- Give numerical tolerance ranges and partial-credit tests.
- Include at least one transfer question, not a verbatim notebook repetition.
- Do not require internet access, personal account sharing, or a notebook not bundled with the exam.
- Keep the complete reference run under 15 minutes on the reference CPU; a prepared student path should be substantially shorter.
- Produce main and retake forms from the same blueprint and moderate both before the main sitting.

## Common performance levels

| Level | Description |
|---|---|
| Excellent | Correct, reproducible, well-tested analysis; choices follow from assumptions and costs; uncertainty and limitations are explicit. |
| Competent | Correct core pipeline and interpretation with minor omissions that do not invalidate conclusions. |
| Developing | Partial technical success but weak validation, testing, or justification; conclusions need qualification. |
| Insufficient | Critical P0 failure, non-reproducible evidence, major leakage/join error, untraceable data, or unsupported conclusions. |

## Assessment production and moderation

For each assessed task, the private repository must contain:

- specification and English copy-edit review;
- concept IDs and priority coverage;
- point rubric and expected completion time;
- public/hidden tests with partial-credit mapping;
- reference solution and clean reference run;
- at least one equivalent variant;
- moderation checklist and reviewer sign-off;
- post-assessment item analysis and issue log;
- release/embargo date, if the assessment will later become public.

