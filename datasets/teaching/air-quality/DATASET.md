# Beijing air-quality teaching slice

## Identity and licence

- Stable source ID: `uci-501`; DOI: `10.24432/C5RK5G`.
- Creator: Song Chen; UCI Machine Learning Repository.
- Licence: Creative Commons Attribution 4.0 International.
- Derived by `tools/build_teaching_data.py` from the checksum-pinned source snapshot.
- No personal data is present in the released tables.

## Composition

`observations.csv` contains 1,008 original hourly rows: three stations × fourteen days, 1–14 March 2013. Values are not statistically imputed or repaired. The observation key is `(station, year, month, day, hour)`. Pollutant measurements, weather variables, wind direction, and station are retained with upstream names and missing values.

`stations.csv` is a three-row registry derived only from the archive: station identifier, upstream source filename, and full upstream row count. It contains no invented geography or station attributes. The relationship from observations to stations is many-to-one.

## Intended use

The slice supports table semantics, timestamps, reshaping, grouping, joins, missingness, data contracts, EDA, and small CPU exercises. It is not a forecasting benchmark and does not represent every Beijing station, other seasons, current conditions, Strasbourg, individual exposure, or causal effects. Hourly rows are temporally dependent.

## Known limitations

The upstream dataset combines air-quality measurements with meteorological observations matched to the nearest weather station. Missing values are present. The short three-station slice changes the population and seasonal coverage of the full 2013–2017 dataset. Any broader claim requires the full snapshot, a declared sampling design, and renewed validation.

Checksums, row counts, and sizes are recorded in `MANIFEST.yml`.
