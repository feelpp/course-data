# Dry Bean teaching table

## Identity and licence

- Stable source ID: `uci-602`; DOI: `10.24432/C50S4B`.
- Creators: Murat Koklu and Ilker Ali Ozkan; UCI Machine Learning Repository.
- Licence: Creative Commons Attribution 4.0 International.
- Derived by lossless ARFF-to-UTF-8-CSV conversion through `tools/build_teaching_data.py`.
- No personal data is present.

## Composition

`observations.csv` contains 13,611 observations, sixteen image-derived numerical shape features, and seven bean classes. One row represents one segmented bean image. The table has no missing values and is therefore unsuitable as the sole data-quality example.

## Intended use

The table supports multiclass softmax/loss exercises, PCA, clustering, cluster validation, and supervised-versus-unsupervised interpretation. The class is available for post-hoc cluster interpretation but must not enter PCA or clustering fitting.

## Known limitations

The observations come from a specific imaging and sampling process. Class labels do not make any clustering the unique “true” partition, and good separation in this table does not establish performance for other cultivars, cameras, acquisition conditions, or populations. Image-derived features are correlated and have different scales.

Checksums, row counts, and sizes are recorded in `MANIFEST.yml`.
