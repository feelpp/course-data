# Controlled source ingest and provenance audit

**Audit date:** 2026-07-18  
**Status:** complete  
**Scope:** `/Users/prudhomm/Downloads/data-20260718T071150Z-1-001.zip` and the three approved UCI dataset snapshots  
**Publication decision:** no raw imported course artifact is approved for publication

## 1. Outcome

The archive has been preserved byte-for-byte, inventoried completely, and isolated from the future public course. All 38 imported items have a checksum, custodial owner, original and normalized names, topic, audience, language, importance candidate, curriculum mapping, provenance and licence status, technical observations, intended destination, disposition, rationale, and rights action.

The archive is useful as a pedagogical mine, but it is not a publishable course. The central decision is therefore to author a new English course using independently written explanations, code, figures, exercises, and assessments. The imported notebooks may inform scope and teaching patterns; they are not source files for automatic translation or direct conversion.

The public-import gate is intentionally empty: **0 of 38 raw artifacts are approved for publication**. This is the only defensible result while 37 notebook licences and copyright holders remain unknown and the remaining PDF is explicitly All Rights Reserved.

## 2. Audit artifacts

- [`source-inventory.csv`](source-inventory.csv): flat register suitable for review in a spreadsheet.
- [`source-inventory.json`](source-inventory.json): full machine-readable technical and provenance record.
- [`../../audit/source-decisions.yml`](../../audit/source-decisions.yml): human-reviewed pedagogical dispositions.
- [`../../audit/source-validation.json`](../../audit/source-validation.json): automated completeness and reference checks.
- [`../../tools/build_source_inventory.py`](../../tools/build_source_inventory.py): reproducible inventory builder.
- [`../../archive/README.md`](../../archive/README.md): raw-archive publication policy.
- [`../../datasets/README.md`](../../datasets/README.md): approved dataset snapshot policy.

The ignored raw archive also contains `MANIFEST.sha256`; it covers the preserved ZIP and all 38 extracted files.

## 3. Archive integrity

| Property | Result |
|---|---|
| Original ZIP size | 24,313,858 bytes |
| Original ZIP SHA-256 | `01df0e0bfd78e2630174f0f7fd6b5cbc45f9af96e4359a74076f8e85b3b93982` |
| Preserved-copy SHA-256 | Identical to the original |
| ZIP entries | 38 |
| Extracted items inventoried | 38 |
| Notebook or notebook-like items | 37 |
| PDF items | 1 |
| Raw items approved for publication | 0 |

The archive copy and extraction live under ignored `archive/raw/` storage. Original filenames, Unicode normalization, extensions, dates, and bytes were preserved. Derived work uses normalized ASCII names; the extensionless Optax notebook is recognized as a notebook and receives an `.ipynb` extension only in derived naming.

## 4. Importance and disposition

Importance is a candidate mapping to the approved P0-P3 course scale, not permission to reuse the source.

| Importance | Meaning for this audit | Items | Interpretation |
|---|---|---:|---|
| P0 Essential | Directly relevant to required data-processing practice | 3 | Mine tabular, pipeline, quality, and EDA ideas first, but rewrite completely. |
| P1 Core | Relevant analytical and statistical-learning content | 17 | Select and compress into the core course; eliminate framework-driven detours. |
| P2 Extension | Optional bridge or advanced context | 5 | Publish only if the 28-hour core is complete and tested. |
| P3 Deferred | Out of scope, obsolete, historical, or owned by another course | 13 | Keep private as reference or transfer conceptually to Scientific Machine Learning. |

Disposition totals are:

| Disposition | Count | Meaning |
|---|---:|---|
| Split and rewrite | 8 | Rebuild as smaller English notes, student tasks, and separate solutions. |
| Rewrite | 1 | Rebuild one compact original lab. |
| Mine and rewrite | 3 | Extract exercise patterns or examples, then redesign independently. |
| Concepts only | 5 | Retain only the topic idea; do not reuse implementation, prose, or figures. |
| Defer to Scientific Machine Learning | 7 | Do not schedule in this course. |
| Private assessment reference | 11 | Keep in the private assessment bank; never copy into the public repository. |
| Historical reference | 1 | Superseded course-plan evidence only. |
| Archive out of scope | 1 | Fourier examination unrelated to the course contract. |
| Exclude from publication | 1 | Third-party kernel PDF with explicit rights restriction. |

## 5. Priority salvage queue

### 5.1 Essential material to rebuild first

1. `SRC-008`, legacy pandas notebook: mine selection, indexing, grouping, reshaping, joins, types, and data-frame assertions. Remove live Strasbourg downloads and geospatial scope from the required path.
2. `SRC-010`, legacy scikit-learn workflow: preserve only the pipeline idea. Replace OECD data and old APIs with the approved course datasets and current leakage-safe pipeline patterns.
3. `SRC-012`, descriptive statistics notebook: mine missing-value, anomaly, and EDA question patterns. Replace absent local files, unattributed examples, and the saved error.

These three sources do not cover the entire P0 curriculum. Provenance, licences, schemas, validated joins, leakage, evaluation design, reproducibility tests, dataset cards, responsible AI, Parquet, and performance-aware processing still require new material.

### 5.2 Core analytical material

The strongest P1 candidates are `SRC-003` to `SRC-007` for Lasso, probabilistic modelling, bias-variance, trees, and ensembles, plus `SRC-022` for classification losses. Each needs English rewriting, explicit outcomes, current APIs, deterministic data, student/solution separation, and tests.

`SRC-009`, `SRC-011`, `SRC-021`, and `SRC-024` are concepts-only references because they either closely follow external repositories, depend on complex framework-specific infrastructure, or combine a core mathematical idea with deferred neural-network content.

### 5.3 JAX boundary

`SRC-014` and `SRC-015` may inspire a short P2 bridge covering arrays, explicit PRNG keys, automatic differentiation, and gradient verification. `SRC-025` may contribute an original two-dimensional diagnostic exercise after rewriting.

Seven JAX/deep-learning notebooks are deferred to Scientific Machine Learning. Manual neural-network construction, PyTrees, Optax training architecture, sentiment models, and optimiser internals cannot displace P0/P1 data-processing outcomes in a 28-hour course.

### 5.4 Assessments

Eleven items are historical examinations, solutions, or assessment-like notebooks. They remain private because they contain solutions, may still reveal reusable question patterns, and have unknown ownership. They can inform difficulty calibration, but new controls and examinations must use new English prompts, new data variants, explicit rubrics, and the approved assessment blueprint.

## 6. Technical health of the notebook collection

The audit performed JSON/notebook validation, cell and output inspection, import extraction, syntax parsing after IPython transformation, URL and local-file discovery, and static detection of network, installation, randomness, and filesystem operations. It did **not** execute raw code.

| Signal | Result | Consequence |
|---|---:|---|
| Notebook-schema validation | 37/37 pass | Files can be parsed, but this does not imply executable correctness. |
| Total cells | 2,250 | Collection is too large for direct conversion. |
| Code cells | 1,076 | Requires selection and redesign, not cosmetic editing. |
| Saved outputs | 771 | Outputs must be stripped and regenerated. |
| Notebooks with outputs lacking a complete execution record | 30 | Saved results are not reproducibility evidence. |
| Notebooks with a saved error output | 1 | Legacy pandas notebook contains an unresolved displayed failure. |
| Notebooks with syntax/incomplete-code flags | 3 | One housing syntax problem and two intentional assessment placeholders. |
| Notebooks using external data or network operations | 13 | Must be replaced by pinned offline inputs. |
| Notebooks installing packages | 2 | Environment mutation must move to the pinned course environment. |
| Notebooks writing or deleting files | 5 | Must be sandboxed or redesigned before execution. |
| Notebooks using randomness | 22 | Determinism must be made explicit. |
| Random notebooks without an apparent seed | 13 | Results may drift between runs. |
| Distinct external URLs | 52 | Each cited source or asset requires review. |
| Distinct imported top-level packages | 32 | Dependency surface is far too broad for the core environment. |

The most frequent imports are Matplotlib (32 notebooks), NumPy (28), `os` (19), pandas (17), TensorFlow (14), JAX (13), and scikit-learn (13). Eight notebooks use Optax. Optional libraries include CVXPY, Graphviz, GeoPandas, Folium, Hyperopt, Statsmodels, PyTorch, and Keras.

Raw execution was deliberately blocked because some cells install system or Python packages, download unpinned data, clone repositories, write pickle files, delete or replace directories, use missing local assets, and expose private solutions. Execution belongs after selected ideas have been rewritten into a pinned environment with controlled datasets and tests.

## 7. Provenance, rights, and language

| Finding | Count |
|---|---:|
| French artifacts | 36 |
| English artifacts | 2 |
| Notebook copyright holder unknown | 37 |
| Notebook licence unknown | 37 |
| Provenance partially indicated by URLs or references | 15 |
| Provenance unknown beyond archive context | 22 |
| Fully identified third-party item | 1 |

The archive contains references to `ageron/handson-ml`, Vincent Vigon asset repositories, public agency downloads, TensorFlow datasets, Google Drive, articles, and research papers. A URL is not a reuse licence. Embedded data images, saved plots, copied diagrams, prose, and code remain non-reusable until origin and rights are documented.

The kernel PDF is *ECE595 / STAT598: Machine Learning I, Lecture 03: Regression with Kernels*, Stanley Chan, Purdue University, Spring 2020. It has 28 pages, and every slide states “All Rights Reserved.” The cover was rendered and visually checked. The PDF remains only in the ignored raw archive and must not be committed, republished, or distributed as course material. If kernel methods are activated as P2, write an original treatment and cite an authorised public source.

Because the course site is English-only, none of the 36 French artifacts can be published as-is. Translation alone would not solve the licensing, structure, execution, or curriculum problems. The required operation is original English redevelopment.

## 8. Dataset snapshots

Three CC BY 4.0 UCI snapshots were downloaded from official endpoints, integrity-tested, pinned by SHA-256, and given source and attribution metadata.

| ID | Role | Snapshot SHA-256 | Integrity |
|---|---|---|---|
| `uci-501` | Beijing air-quality semester spine | `d1b9261c54132f04c374f762f1e5e512af19f95c95fd6bfa1e8ac7e927e3b0b8` | Valid nested ZIP; 12 station CSV files |
| `uci-601` | AI4I industrial classification | `f601f14294bcf190f9d720676b7f0aea46a26cde9ab8ebc7b4f8174d9d26b252` | Valid ZIP; one CSV |
| `uci-602` | Dry Bean multiclass reserve | `0a64eff5be87f48c3dbbfc0a12a56c5d5b5167ef8e61cd45d69b3e7c7130c06f` | Valid ZIP; ARFF, XLSX, and documentation |

### UCI-501 upstream-package anomaly

The official UCI-501 download retrieved on 2026-07-18 was not a clean dataset bundle. Alongside the genuine `PRSA2017_Data_20130301-20170228.zip`, it contained:

- an 828×828 JPEG with Instagram metadata;
- `data.csv`, containing stock prices;
- `test.csv`, containing different stock prices.

These files are unrelated to Beijing air quality and cannot safely inherit the dataset licence. The complete official download is retained in ignored quarantine for evidence. Only the nested PRSA2017 ZIP was promoted to the reviewed snapshot. This curation decision is recorded in `datasets/snapshots/uci-501/SOURCE.yml`.

### Remaining dataset work

The snapshots are licensed source inputs, not student-ready bundles. The next implementation work must produce deterministic transformations, schemas, datasheets, small CI samples, data-quality assertions, attribution in every derived bundle, and fixed split recipes. The AI4I failure-type columns must be excluded from predictors when the aggregate failure flag is the target, because they encode how that target was constructed.

## 9. Risks and controls

| Risk | Level | Control |
|---|---|---|
| Accidental publication of solutions or exams | Critical | Entire raw archive ignored; assessment destinations are private only. |
| Copyright infringement | Critical | No raw notebook or PDF approved; clean-room English redevelopment required. |
| Dataset contamination | Critical | Inspect archive contents, pin checksums, curate UCI-501, validate schemas before use. |
| Unreproducible saved outputs | High | Strip all outputs, execute from clean environments, compare reviewed metrics and figures. |
| Live downloads and missing assets | High | Bundle licensed snapshots and offline examination variants. |
| Framework overload | High | Keep JAX optional; move neural-network implementation to Scientific Machine Learning. |
| Obsolete or conflicting APIs | Medium | Pin a current environment and rewrite against reviewed APIs. |
| Excess dependency surface | Medium | Keep the required environment small; isolate optional extras. |

## 10. Acceptance record

The controlled-ingest work passes its acceptance gate:

- 38 of 38 imported artifacts are inventoried and checksum-addressable;
- every artifact has a custodial owner, provenance state, licence state, importance candidate, disposition, destination, and rights action;
- every curriculum concept reference is valid;
- normalized derived names are unique;
- all raw artifacts are quarantined and zero are silently public;
- instructor solutions and historical examinations are routed only to a future private repository;
- the All Rights Reserved PDF is excluded;
- dataset sources, licences, attribution, retrieval dates, and checksums are recorded;
- the contaminated UCI-501 package has been safely curated;
- all generated repository documentation is in English.

The next work package can therefore concentrate on repository and Antora implementation without importing unresolved raw content into the public site.

