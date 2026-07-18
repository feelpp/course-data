# Dataset decision and shortlist

## Selection criteria

Course datasets must be:

- relevant to scientific research or industrial practice;
- distributable under a clear licence with stable citation/DOI;
- free of personal/confidential data for the baseline course;
- usable offline from a versioned snapshot;
- rich enough for quality, types, missingness, grouping, joins, EDA, supervised or unsupervised analysis;
- small enough for ordinary laptops while large enough to motivate performance-aware processing;
- suitable for deterministic CI samples and assessment variants.

## Selected semester spine

### Beijing Multi-Site Air Quality

- Source: [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/501/beijing%2Bmulti%2Bsite%2Bair%2Bquality%2Bdata)
- DOI: [10.24432/C5RK5G](https://doi.org/10.24432/C5RK5G)
- Licence: CC BY 4.0
- Scale: 420,768 hourly observations from 12 monitoring sites, March 2013–February 2017
- Variables: six pollutants, meteorological variables, time components, wind direction, and station
- Missing values: yes
- Primary domains: environment, sensors, time series, scientific data

### Why it is the spine

It supports most of the course without becoming a toy:

- concatenate and validate multiple station files;
- construct a timestamp and verify continuity/duplicates;
- handle units, categorical wind direction, missing observations, impossible ranges, and station metadata;
- reshape and aggregate by time/station;
- demonstrate temporal and group leakage;
- build regression baselines for pollutant concentration;
- create derived threshold classification only when the threshold source and purpose are documented;
- use PCA and clustering for station/pollution profiles;
- compare CSV with Parquet, column selection, filtered reads, memory use, and query pushdown;
- write a meaningful dataset datasheet and limitations section.

### Data preparation plan

Preserve the original zip and create reproducible derived artifacts:

1. `raw/` snapshot with upstream filename and SHA-256;
2. `observations.parquet`, one validated hourly table;
3. `stations.csv`, a derived station-key table containing only documented metadata available from the source, plus explicit `unknown` values where metadata is unavailable;
4. `sample/observations_sample.parquet` for CI and introductory tasks;
5. schema files with units, types, allowed categories, nullability, and range rules;
6. a datasheet documenting that weather observations are matched to the nearest weather station and that the dataset is historical Beijing data, not a Strasbourg air-quality proxy;
7. split recipes for temporal, station-held-out, and ordinary random comparisons, with random splitting labelled as inappropriate for forecasting claims.

No live UCI download is performed during normal notebooks or assessments.

## Selected industrial classification case

### AI4I 2020 Predictive Maintenance

- Source: [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/601/ai4i)
- DOI: [10.24432/C5HS5C](https://doi.org/10.24432/C5HS5C)
- Licence: CC BY 4.0
- Scale: 10,000 synthetic industrial observations
- Tasks: classification/regression; rare machine-failure outcome
- Personal data: none

### Why it is selected

It adds an industrial context, class imbalance, asymmetric error costs, thresholds, failure analysis, and a compact CPU-friendly assessment/project dataset. Because the dataset includes failure-mode columns related to the aggregate machine-failure target, feature roles must be reviewed carefully: target and post-outcome/failure indicators must never leak into the predictors.

Its synthetic nature must be stated prominently. Students may not generalise measured performance to a real factory without external validation.

## Optional multiclass reserve

### Dry Bean

- Source: [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/602/dry%2Bbean%2Bdataset)
- DOI: [10.24432/C50S4B](https://doi.org/10.24432/C50S4B)
- Licence: CC BY 4.0
- Scale: 13,611 observations, 16 image-derived shape features, seven classes

Use only when a clean multiclass/PCA/clustering transfer task is needed. It does not replace the messy spine dataset because it has no missing values and limited wrangling complexity.

## Synthetic oracle datasets

Versioned generators will create small datasets for:

- ill-conditioned least squares and stable solver comparison;
- Ridge/Lasso coefficient paths;
- bias–variance and learning curves;
- obvious target leakage and group/temporal leakage;
- imbalanced classification and threshold costs;
- clusters with spherical, anisotropic, varying-density, and noise structures;
- metric and transformation tests with known answers.

Generators declare seeds and mathematical ground truth. Generated data are rebuilt in CI and are not treated as evidence about a real population.

## Rejected as the primary spine

| Candidate | Decision | Reason |
|---|---|---|
| MNIST | Optional demonstration only | Clean benchmark; little provenance, joining, schema, missingness, or industrial/scientific table work; overused in the archive. |
| California housing / old housing notebook | Do not use as primary | Existing notebook has adaptation/provenance concerns and a dated remote-download workflow. |
| IMDB sentiment | Defer to optional NLP/SciML material | High framework/runtime overhead and weak alignment with S1 data-processing priorities. |
| Dry Bean | Reserve | Excellent clean multiclass data but insufficient messiness and scale for the lifecycle spine. |
| AI4I | Secondary, not spine | Strong industrial classification case but small, synthetic, and without missing values. |

## Data-governance requirements

Before a dataset enters a released course bundle, the data steward must approve:

- exact upstream source and DOI;
- licence text and attribution wording;
- snapshot date, upstream filename, size, and SHA-256;
- raw/derived distinction and transformation provenance;
- schema, units, categories, missing-value conventions, and target/feature roles;
- privacy and ethical-use note;
- datasheet and citation entry;
- CI sample representativeness and known limitations;
- offline fetch/cache procedure;
- assessment embargo status when data contain hidden variants.

The public repository stores small licensed snapshots when redistribution is appropriate. Larger originals may use a checksum-verified fetch script, but course execution uses a prepared cache and never assumes network availability.
