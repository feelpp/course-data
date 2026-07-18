# Data Processing and Mining — course contract

## Identity

- Programme: Master CSMI, M1 Semester 1
- Credits: 3 ECTS
- Contact time: 28 hours
- Course-site language: English
- Public component identifier: `course-data`

## Course purpose

This course prepares applied-mathematics students to turn raw scientific or industrial data into a reproducible, leakage-safe, computationally reasoned analysis. Statistical learning is taught as part of the full data lifecycle rather than as model fitting in isolation.

## Course promise

By the end of the course, a student can take a documented dataset from raw tables to a reproducible analysis; validate and transform it; build and compare defensible baselines, supervised models, or clusters; quantify and interpret performance and uncertainty; and deliver tested code, data documentation, and a concise technical report.

## Entry profile and prerequisites

The course assumes mathematical maturity at Bachelor level, including basic linear algebra, calculus, probability, and statistics. Students should have introductory Python experience, but the diagnostic recognises that programming fluency will vary.

Required before Block 2:

- run Python and Jupyter in the supported environment;
- use variables, functions, loops/comprehensions, imports, and exceptions;
- read basic NumPy array code;
- clone/pull a repository and run a documented command.

Students who do not meet the diagnostic threshold receive a short remedial path. Contact time is not converted into a general Python course.

## Learning outcomes

After successful completion, students can:

1. formulate a data question and identify the unit of analysis, target, stakeholders, assumptions, and risks;
2. document source, licence, provenance, privacy, schema, types, units, missingness, duplicates, anomalies, and representativeness;
3. combine and transform tabular data using validated joins, reshaping, grouping, and executable quality checks;
4. produce reproducible exploratory analysis and truthful visualisations;
5. construct leakage-safe preprocessing and evaluation pipelines for heterogeneous features;
6. select and interpret baselines, splits, cross-validation, metrics, thresholds, and failure analyses;
7. explain and apply stable linear regression, likelihood/loss links, logistic regression, Ridge/Lasso, bias–variance, trees, forests, boosting at introductory depth, PCA, and clustering;
8. reason about computational complexity, memory, dtypes, columnar storage, and query-before-materialisation workflows;
9. test transformations and metrics with toy oracles and execute the analysis from a clean checkout;
10. write a dataset datasheet, result/model card, limitations statement, and AI-assistance declaration;
11. explain how vectorised data workflows connect to downstream JAX, SciML, and HPC topics.

## Teaching pattern

The baseline is fourteen two-hour blocks. A typical block contains:

- 20–30 minutes of concept development;
- 30–45 minutes of guided analysis;
- 35–50 minutes of individual or pair work;
- 10–20 minutes of written interpretation, testing, and debrief.

Exercises require predictions and explanations before or alongside code execution. Library use is encouraged after the method, assumptions, and failure modes are understood.

## Required student artifacts

- clean student notebooks or scripts;
- executable data checks and tests;
- reproducible locked environment;
- dataset provenance/licence record;
- dataset datasheet and result/model card for the mini-project;
- concise figures and technical interpretation;
- `ai-notes/` log whenever AI assistance is allowed and used;
- tagged project release at the assessed commit.

## Assessment summary

| Assessment | Weight | Default AI mode | Core evidence |
|---|---:|---|---|
| Control 1 | 20% | A | Data audit, validated join, quality checks, leakage-safe baseline. |
| Mini-project | 25% | B | Reproducible repository, tests, analysis, datasheet/result card, individual verification. |
| Control 2 | 15% | A | Audit of a flawed analysis and short concept interpretation. |
| Final exam | 40% | A | Integrated data, mathematical, implementation, evaluation, and reproducibility competence. |

Detailed coverage and rubrics are defined in `assessment-blueprint.md`.

## Language contract

All official student-facing material is in English. Students are expected to use clear technical English in reports, notebooks, figure labels, code documentation, and assessment responses. Language quality is assessed only where it affects technical clarity; it does not replace evaluation of mathematical and computational correctness. Approved accommodations are handled individually.

## Reproducibility contract

P0/P1 work must run on the documented CPU environment from a clean checkout without network access after datasets and dependencies have been prepared. Results with stochastic elements declare seeds and acceptable tolerances. Hardware speed does not determine marks.

## Integrity, privacy, and AI contract

Students remain responsible for every claim, equation, citation, figure, and code fragment. They must cite primary sources, disclose allowed AI assistance, independently verify suggestions, and never upload confidential, personal, examination, embargoed, or hidden-test material to external services.

## Completion standard

Passing the course requires more than a high predictive score. A submission can be judged insufficient when it contains a critical P0 failure such as an invalid join, test leakage, untraceable/unlicensed data, a non-reproducible pipeline, fabricated evidence, or an undisclosed prohibited assistance mode.

