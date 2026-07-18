# Dataset snapshots

This directory contains reviewed, checksum-pinned source snapshots for course preparation. Each snapshot has source, citation, licence, retrieval, integrity, and intended-use metadata in `SOURCE.yml`.

The datasets are distributed under the Creative Commons Attribution 4.0 International licence. Course pages, notebooks, derived data, and student bundles must retain the attribution and DOI recorded for the relevant dataset.

The snapshots are immutable preparation inputs. Reviewed classroom tables are generated deterministically under `datasets/teaching/` by `uv run python tools/build_teaching_data.py`. Each teaching directory has a checksum manifest and is published with the student notebooks.

## Included snapshots

| ID | Role | Dataset |
|---|---|---|
| `uci-501` | Semester spine | Beijing Multi-Site Air Quality |
| `uci-601` | Industrial classification case | AI4I 2020 Predictive Maintenance |
| `uci-602` | Optional multiclass reserve | Dry Bean |

## Teaching tables

| Directory | Source | Scope |
|---|---|---|
| `teaching/air-quality` | `uci-501` | First fourteen days of March 2013 for Aotizhongxin, Changping, and Dingling, plus a source-file station registry. |
| `teaching/predictive-maintenance` | `uci-601` | Complete 10,000-row synthetic industrial table. Failure-mode fields are explicitly target-derived leakage for the aggregate failure outcome. |

The air-quality slice is not representative of all Beijing stations, seasons, current conditions, or another city. AI4I is synthetic and cannot establish performance in a real factory. These limits must remain in student reports and result cards.

## Licence

The snapshots are provided under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Attribution does not imply that the dataset creators or UCI endorse this course or its derived material.
