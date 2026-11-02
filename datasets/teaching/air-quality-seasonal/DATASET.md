# Beijing seasonal-window teaching supplement

Source: Song Chen, Beijing Multi-Site Air Quality, UCI 501,
DOI 10.24432/C5RK5G, CC BY 4.0. Derived without changing measured values
from the repository's checksum-pinned `datasets/snapshots/uci-501/source.zip`.

Rebuild: `uv run python teaching/sessions/multivariate/build_seasonal_data.py`.
The script verifies the snapshot checksum before extraction.

The 4,032 rows are the first fourteen days of March, June, September and
December 2013, at Aotizhongxin, Changping and Dingling (336 hours per window
and station). The 18 columns and units match `air-quality/observations.csv`;
`source_row` is the original upstream row number. Missing values are retained.
The March rows repeat the original teaching slice deliberately; these tables
must not be concatenated as if they were disjoint samples.

Use the four windows to challenge pooled correlations and compare station
and time contexts. Spring/summer/autumn/winter labels identify selected
Northern Hemisphere calendar windows. They do not make fourteen days
representative of a season. Station-hours are dependent; stations also share
weather. This is neither a seasonal climatology nor an independent test set.
No causal or present-day pollution claim follows from this extract.
