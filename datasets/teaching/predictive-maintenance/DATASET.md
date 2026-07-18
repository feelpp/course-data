# AI4I predictive-maintenance teaching table

## Identity and licence

- Stable source ID: `uci-601`; DOI: `10.24432/C5HS5C`.
- Creator/reference author: S. Matzka; UCI Machine Learning Repository.
- Licence: Creative Commons Attribution 4.0 International.
- Derived by lossless CSV extraction through `tools/build_teaching_data.py` from the checksum-pinned source snapshot.
- The dataset is synthetic and contains no personal data.

## Composition and roles

`observations.csv` contains 10,000 rows with product type, air/process temperature, rotational speed, torque, tool wear, aggregate machine-failure label, and five failure-mode indicators.

`UDI` and `Product ID` are identifiers. `Machine failure` is the aggregate target in the course exercise. `TWF`, `HDF`, `PWF`, `OSF`, and `RNF` encode failure modes used to construct or explain that target and therefore must not be used as pre-outcome predictors. Their exclusion is a P0 feature-time/leakage requirement.

## Intended use

The table supports leakage audits, heterogeneous preprocessing pipelines, rare-outcome baselines, metrics, thresholds, and error analysis on ordinary CPUs. It is not evidence that a workflow will perform in a real plant.

## Known limitations

The synthetic generator simplifies real measurement, maintenance, temporal, operator, and deployment processes. The course random split is a controlled row-level exercise, not a future-time or factory-generalisation claim. Operational use would require real representative data, decision-time feature validation, temporal/site evaluation, calibration, safety review, monitoring, and human-process integration.

Checksums, row counts, and sizes are recorded in `MANIFEST.yml`.
