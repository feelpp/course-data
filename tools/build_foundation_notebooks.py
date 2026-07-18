#!/usr/bin/env python3
"""Build reviewed canonical notebooks for the P0 foundation sequence."""

from __future__ import annotations

from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "notebooks" / "instructor" / "foundations"


def markdown(source: str, tags: list[str] | None = None):
    return nbformat.v4.new_markdown_cell(source, metadata={"tags": tags or []})


def code(
    source: str,
    tags: list[str] | None = None,
    student_source: str | None = None,
):
    metadata: dict = {"tags": tags or []}
    if student_source is not None:
        metadata["course"] = {"student_source": student_source}
    return nbformat.v4.new_code_cell(source, metadata=metadata)


def notebook(metadata: dict, cells: list) -> nbformat.NotebookNode:
    return nbformat.v4.new_notebook(
        cells=cells,
        metadata={
            "course": metadata,
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.12"},
        },
    )


LOCATOR = """from pathlib import Path

def locate(relative: str, local_name: str | None = None) -> Path:
    candidates = []
    if local_name:
        candidates.append(Path.cwd() / local_name)
    candidates.extend(root / relative for root in [Path.cwd(), *Path.cwd().parents])
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        f"Cannot find {relative}. Run from the course clone or place the downloaded data beside this notebook."
    )
"""


def build_tabular() -> None:
    meta = {
        "assessed": True,
        "concept_ids": ["DP-ARR-01", "DP-TAB-01", "DP-TAB-02", "DP-TAB-03", "DP-QLT-01"],
        "difficulty": "D2",
        "duration_minutes": 90,
        "execution_profile": "fast",
        "language": "en",
        "outcomes": ["LO2", "LO3", "LO8"],
        "prerequisites": ["Readiness check"],
        "priority": "P0",
    }
    cells = [
        markdown(
            "# Arrays, tidy tables, and validated joins\n\n**P0 Essential · D2 Independent · 90 minutes**"
        ),
        code("import pandas as pd\n\n" + LOCATOR, ["setup"]),
        code(
            "obs_path = locate('datasets/teaching/air-quality/observations.csv', 'observations.csv')\n"
            "stations_path = locate('datasets/teaching/air-quality/stations.csv', 'stations.csv')\n"
            "observations = pd.read_csv(obs_path)\n"
            "stations = pd.read_csv(stations_path)\n"
            "observations.shape, stations.shape",
            ["setup"],
        ),
        markdown(
            "## Predict before running\n\nWhat should uniquely identify one hourly station observation? What join cardinality connects observations to the station registry?"
        ),
        markdown(
            "## Task\n\nConstruct a timestamp, validate the observation key, produce a tidy pollutant table, and join the registry without changing the observation-key set."
        ),
        code(
            "def prepare_tables(observations: pd.DataFrame, stations: pd.DataFrame):\n"
            "    frame = observations.copy()\n"
            "    frame['timestamp'] = pd.to_datetime(frame[['year', 'month', 'day', 'hour']])\n"
            "    key = ['station', 'timestamp']\n"
            "    if frame.duplicated(key).any():\n"
            "        raise ValueError('Observation key is not unique')\n"
            "    pollutants = frame.melt(\n"
            "        id_vars=key, value_vars=['PM2.5', 'PM10', 'NO2'],\n"
            "        var_name='pollutant', value_name='concentration'\n"
            "    )\n"
            "    before = set(map(tuple, frame[key].itertuples(index=False, name=None)))\n"
            "    joined = frame.merge(stations, on='station', how='left', validate='many_to_one', indicator=True)\n"
            "    after = set(map(tuple, joined[key].itertuples(index=False, name=None)))\n"
            "    if before != after or not joined['_merge'].eq('both').all():\n"
            "        raise ValueError('Join changed or failed to match observation keys')\n"
            "    return joined.drop(columns='_merge'), pollutants",
            ["solution"],
            "def prepare_tables(observations: pd.DataFrame, stations: pd.DataFrame):\n"
            "    # TODO: construct timestamp, validate keys, reshape, and validate the join.\n"
            "    raise NotImplementedError\n",
        ),
        code(
            "joined, pollutants = prepare_tables(observations, stations)\n"
            "assert joined[['station', 'timestamp']].duplicated().sum() == 0\n"
            "assert len(joined) == len(observations)\n"
            "assert set(pollutants['pollutant']) == {'PM2.5', 'PM10', 'NO2'}\n"
            "assert len(pollutants) == 3 * len(observations)\n"
            "joined[['station', 'timestamp', 'PM2.5', 'source_file']].head()",
            ["test-public"],
        ),
        markdown(
            "## Transfer\n\nCreate a daily station summary. State its unit and key, preserve missingness, and assert uniqueness. Explain why row-count equality alone would not prove join correctness."
        ),
        markdown(
            "**Instructor note.** Require students to compare key sets, not only row counts, and to explain storage dtype versus semantic role.",
            ["instructor-only"],
        ),
    ]
    nbformat.write(notebook(meta, cells), OUTPUT / "tabular-data.ipynb")


def build_quality() -> None:
    meta = {
        "assessed": True,
        "concept_ids": ["DP-QLT-01", "DP-QLT-02", "DP-QLT-03", "DP-QLT-04", "DP-TST-01"],
        "difficulty": "D2",
        "duration_minutes": 90,
        "execution_profile": "fast",
        "language": "en",
        "outcomes": ["LO2", "LO3", "LO4", "LO5", "LO9"],
        "prerequisites": ["Validated joins"],
        "priority": "P0",
    }
    cells = [
        markdown(
            "# Data quality, missingness, and anomalies\n\n**P0 Essential · D2 Independent · 90 minutes**"
        ),
        code("import pandas as pd\n\n" + LOCATOR, ["setup"]),
        code(
            "path = locate('datasets/teaching/air-quality/observations.csv', 'observations.csv')\n"
            "clean = pd.read_csv(path).head(80)\n"
            "quality = clean.copy()\n"
            "quality['temperature_unit'] = 'C'\n"
            "quality.loc[3, ['TEMP', 'temperature_unit']] = [quality.loc[3, 'TEMP'] * 9 / 5 + 32, 'F']\n"
            "quality.loc[7, 'wd'] = 'INVALID'\n"
            "quality.loc[11, 'WSPM'] = -2.0\n"
            "quality = pd.concat([quality, quality.iloc[[5]]], ignore_index=True)\n"
            "quality.tail(3)",
            ["setup"],
        ),
        markdown(
            "## Task\n\nAudit identity, missingness, units, category vocabulary, range validity, and anomalies. Repair only rules justified by the provided contract."
        ),
        code(
            "def audit_quality(frame: pd.DataFrame) -> dict[str, int]:\n"
            "    key = ['station', 'year', 'month', 'day', 'hour']\n"
            "    valid_wind = {'N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW'}\n"
            "    return {\n"
            "        'duplicate_rows': int(frame.duplicated(key, keep=False).sum()),\n"
            "        'missing_pm25': int(frame['PM2.5'].isna().sum()),\n"
            "        'non_celsius_rows': int(frame['temperature_unit'].ne('C').sum()),\n"
            "        'invalid_wind': int((frame['wd'].notna() & ~frame['wd'].isin(valid_wind)).sum()),\n"
            "        'negative_wind_speed': int(frame['WSPM'].lt(0).sum()),\n"
            "    }",
            ["solution"],
            "def audit_quality(frame: pd.DataFrame) -> dict[str, int]:\n"
            "    # TODO: return focused counts for identity, missingness, units, categories, and ranges.\n"
            "    raise NotImplementedError\n",
        ),
        code(
            "audit = audit_quality(quality)\n"
            "assert audit['duplicate_rows'] == 2\n"
            "assert audit['non_celsius_rows'] == 1\n"
            "assert audit['invalid_wind'] == 1\n"
            "assert audit['negative_wind_speed'] == 1\n"
            "audit",
            ["test-public"],
        ),
        markdown(
            "## Decisions\n\nConvert the known Fahrenheit row, quarantine the invalid category and impossible negative speed, and distinguish the exact duplicate from a repeated event. Do not impute PM2.5 here: any learned imputation belongs inside the modelling pipeline."
        ),
        code(
            "repaired = quality.copy()\n"
            "is_f = repaired['temperature_unit'].eq('F')\n"
            "repaired.loc[is_f, 'TEMP'] = (repaired.loc[is_f, 'TEMP'] - 32) * 5 / 9\n"
            "repaired.loc[is_f, 'temperature_unit'] = 'C'\n"
            "repaired = repaired.drop_duplicates(['station','year','month','day','hour'])\n"
            "repaired.loc[~repaired['wd'].isin(clean['wd'].dropna().unique()), 'wd'] = pd.NA\n"
            "repaired.loc[repaired['WSPM'].lt(0), 'WSPM'] = pd.NA\n"
            "assert audit_quality(repaired)['duplicate_rows'] == 0",
            ["solution"],
            "# TODO: implement only the justified repairs, then rerun the audit.\nrepaired = quality.copy()\n",
        ),
        markdown(
            "## Transfer\n\nWrite a data-contract table with rule, severity, observed count, decision, and evidence. Explain which finding blocks modelling and which requires sensitivity/domain review."
        ),
    ]
    nbformat.write(notebook(meta, cells), OUTPUT / "data-quality.ipynb")


def build_eda() -> None:
    meta = {
        "assessed": True,
        "concept_ids": ["DP-EDA-01", "DP-SMP-01", "DP-QLT-04"],
        "difficulty": "D2",
        "duration_minutes": 80,
        "execution_profile": "fast",
        "language": "en",
        "outcomes": ["LO1", "LO2", "LO4", "LO6"],
        "prerequisites": ["Data-quality audit"],
        "priority": "P0",
    }
    cells = [
        markdown(
            "# Exploratory analysis and sampling\n\n**P0 Essential · D2 Independent · 80 minutes**"
        ),
        code("import matplotlib.pyplot as plt\nimport pandas as pd\n\n" + LOCATOR, ["setup"]),
        code(
            "path = locate('datasets/teaching/air-quality/observations.csv', 'observations.csv')\n"
            "air = pd.read_csv(path)\n"
            "air['timestamp'] = pd.to_datetime(air[['year','month','day','hour']])\n"
            "air.shape",
            ["setup"],
        ),
        markdown(
            "## Predict before plotting\n\nName one claim this three-station, fourteen-day sample can support and one it cannot. What dependence makes a random row split questionable for forecasting?"
        ),
        code(
            "def coverage_table(frame: pd.DataFrame) -> pd.DataFrame:\n"
            "    return (frame.groupby('station', observed=True)\n"
            "            .agg(rows=('timestamp','size'), start=('timestamp','min'), end=('timestamp','max'),\n"
            "                 pm25_missing=('PM2.5', lambda s: int(s.isna().sum())))\n"
            "            .reset_index())",
            ["solution"],
            "def coverage_table(frame: pd.DataFrame) -> pd.DataFrame:\n"
            "    # TODO: report rows, time coverage, and PM2.5 missingness by station.\n"
            "    raise NotImplementedError\n",
        ),
        code(
            "coverage = coverage_table(air)\n"
            "assert set(coverage.columns) == {'station','rows','start','end','pm25_missing'}\n"
            "assert coverage['rows'].sum() == len(air)\n"
            "coverage",
            ["test-public"],
        ),
        code(
            "fig, ax = plt.subplots(figsize=(8, 4))\n"
            "for station, group in air.groupby('station'):\n"
            "    daily = group.set_index('timestamp')['PM2.5'].resample('D').mean()\n"
            "    ax.plot(daily.index, daily, marker='o', label=station)\n"
            "ax.set(title='Daily mean PM2.5 in the teaching slice', ylabel='PM2.5 (µg/m³)', xlabel='Date')\n"
            "ax.legend()\n"
            "fig.autofmt_xdate()\n"
            "plt.show()",
            ["demo"],
        ),
        markdown(
            "## Independent brief\n\nCreate exactly three figures: coverage/missingness, a distribution with extremes, and one stratified relationship. Every caption must report the analysis count and one limitation. Do not claim that this slice represents all stations, seasons, cities, or current conditions."
        ),
        markdown(
            "**Instructor note.** Assess the claim/figure/sample connection, not visual decoration. Ask how missingness and autocorrelation change interpretation.",
            ["instructor-only"],
        ),
    ]
    nbformat.write(notebook(meta, cells), OUTPUT / "eda-sampling.ipynb")


def build_safe_pipeline() -> None:
    meta = {
        "assessed": True,
        "concept_ids": [
            "DP-EVAL-01",
            "DP-EVAL-02",
            "DP-PIPE-01",
            "DP-EVAL-03",
            "DP-QLT-02",
            "DP-TST-01",
        ],
        "difficulty": "D3",
        "duration_minutes": 110,
        "execution_profile": "fast",
        "language": "en",
        "outcomes": ["LO2", "LO5", "LO6", "LO9"],
        "prerequisites": ["Sampling", "Data quality"],
        "priority": "P0",
    }
    cells = [
        markdown(
            "# Leakage-safe pipelines and baselines\n\n**P0 Essential · D3 Synthesis · 110 minutes**"
        ),
        code(
            "import pandas as pd\n"
            "from sklearn.compose import ColumnTransformer\n"
            "from sklearn.dummy import DummyClassifier\n"
            "from sklearn.impute import SimpleImputer\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.metrics import average_precision_score\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.preprocessing import OneHotEncoder, StandardScaler\n\n" + LOCATOR,
            ["setup"],
        ),
        code(
            "path = locate('datasets/teaching/predictive-maintenance/observations.csv', 'observations.csv')\n"
            "machines = pd.read_csv(path)\n"
            "machines['Machine failure'].value_counts(normalize=True).sort_index()",
            ["setup"],
        ),
        markdown(
            "## Feature-time audit\n\n`TWF`, `HDF`, `PWF`, `OSF`, and `RNF` are failure-mode indicators used to construct the aggregate target. They are not predictors available before the outcome. `UDI` and `Product ID` are identifiers, not default predictive features."
        ),
        code(
            "def make_split(frame: pd.DataFrame):\n"
            "    target = 'Machine failure'\n"
            "    excluded = ['UDI','Product ID',target,'TWF','HDF','PWF','OSF','RNF']\n"
            "    X = frame.drop(columns=excluded)\n"
            "    y = frame[target]\n"
            "    return train_test_split(X, y, test_size=0.25, random_state=20260718, stratify=y)\n\n"
            "def make_pipeline() -> Pipeline:\n"
            "    numeric = ['Air temperature [K]','Process temperature [K]','Rotational speed [rpm]',\n"
            "               'Torque [Nm]','Tool wear [min]']\n"
            "    categorical = ['Type']\n"
            "    preprocessing = ColumnTransformer([\n"
            "        ('num', Pipeline([('impute', SimpleImputer(strategy='median')), ('scale', StandardScaler())]), numeric),\n"
            "        ('cat', Pipeline([('impute', SimpleImputer(strategy='most_frequent')),\n"
            "                          ('encode', OneHotEncoder(handle_unknown='ignore'))]), categorical),\n"
            "    ])\n"
            "    return Pipeline([('preprocess', preprocessing),\n"
            "                     ('model', LogisticRegression(max_iter=1000, class_weight='balanced'))])",
            ["solution"],
            "def make_split(frame: pd.DataFrame):\n"
            "    # TODO: exclude identifiers, target, and every target-derived failure indicator; split first.\n"
            "    raise NotImplementedError\n\n"
            "def make_pipeline() -> Pipeline:\n"
            "    # TODO: put numeric/categorical learned preprocessing and the model in one pipeline.\n"
            "    raise NotImplementedError\n",
        ),
        code(
            "X_train, X_test, y_train, y_test = make_split(machines)\n"
            "assert not {'TWF','HDF','PWF','OSF','RNF','Machine failure'} & set(X_train.columns)\n"
            "model = make_pipeline().fit(X_train, y_train)\n"
            "dummy = DummyClassifier(strategy='prior').fit(X_train, y_train)\n"
            "model_ap = average_precision_score(y_test, model.predict_proba(X_test)[:, 1])\n"
            "dummy_ap = average_precision_score(y_test, dummy.predict_proba(X_test)[:, 1])\n"
            "assert model_ap > dummy_ap\n"
            "{'model_pr_auc': model_ap, 'dummy_pr_auc': dummy_ap}",
            ["test-public"],
        ),
        markdown(
            "## Transfer\n\nRepair a version that imputes globally and retains `HDF`. Explain the split and feature-time boundary, add a leakage assertion, and state why this synthetic random split is not evidence of future factory performance."
        ),
    ]
    nbformat.write(notebook(meta, cells), OUTPUT / "safe-pipelines.ipynb")


def build_metrics() -> None:
    meta = {
        "assessed": True,
        "concept_ids": ["DP-MET-02", "DP-EVAL-03", "DP-THR-01", "DP-INT-01"],
        "difficulty": "D2",
        "duration_minutes": 90,
        "execution_profile": "fast",
        "language": "en",
        "outcomes": ["LO4", "LO6", "LO10"],
        "prerequisites": ["Leakage-safe pipeline"],
        "priority": "P0",
    }
    cells = [
        markdown(
            "# Metrics, thresholds, and error analysis\n\n**P0 Essential · D2 Independent · 90 minutes**"
        ),
        code(
            "import numpy as np\n"
            "import pandas as pd\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.metrics import (average_precision_score, confusion_matrix, precision_score,\n"
            "                             recall_score, roc_auc_score)\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.pipeline import make_pipeline\n"
            "from sklearn.preprocessing import OneHotEncoder, StandardScaler\n"
            "from sklearn.compose import ColumnTransformer\n\n" + LOCATOR,
            ["setup"],
        ),
        code(
            "path = locate('datasets/teaching/predictive-maintenance/observations.csv', 'observations.csv')\n"
            "data = pd.read_csv(path)\n"
            "features = ['Type','Air temperature [K]','Process temperature [K]',\n"
            "            'Rotational speed [rpm]','Torque [Nm]','Tool wear [min]']\n"
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    data[features], data['Machine failure'], test_size=0.25, random_state=20260718,\n"
            "    stratify=data['Machine failure'])\n"
            "pre = ColumnTransformer([('type', OneHotEncoder(handle_unknown='ignore'), ['Type']),\n"
            "                         ('num', StandardScaler(), features[1:])])\n"
            "model = make_pipeline(pre, LogisticRegression(max_iter=1000, class_weight='balanced'))\n"
            "model.fit(X_train, y_train)\n"
            "scores = model.predict_proba(X_test)[:, 1]",
            ["setup"],
        ),
        markdown(
            "## Task\n\nBuild a threshold report containing the confusion counts, precision, and recall. Keep the positive class and matrix orientation explicit."
        ),
        code(
            "def threshold_report(y_true, scores, threshold: float) -> dict[str, float | int]:\n"
            "    prediction = np.asarray(scores) >= threshold\n"
            "    tn, fp, fn, tp = confusion_matrix(y_true, prediction, labels=[0, 1]).ravel()\n"
            "    return {'threshold': threshold, 'tn': int(tn), 'fp': int(fp), 'fn': int(fn), 'tp': int(tp),\n"
            "            'precision': precision_score(y_true, prediction, zero_division=0),\n"
            "            'recall': recall_score(y_true, prediction, zero_division=0)}",
            ["solution"],
            "def threshold_report(y_true, scores, threshold: float) -> dict[str, float | int]:\n"
            "    # TODO: return TN, FP, FN, TP, precision, and recall for positive class 1.\n"
            "    raise NotImplementedError\n",
        ),
        code(
            "reports = pd.DataFrame([threshold_report(y_test, scores, t) for t in (0.3, 0.5, 0.7)])\n"
            "assert (reports[['tn','fp','fn','tp']].sum(axis=1) == len(y_test)).all()\n"
            "summary = {'roc_auc': roc_auc_score(y_test, scores),\n"
            "           'pr_auc': average_precision_score(y_test, scores),\n"
            "           'prevalence': float(y_test.mean())}\n"
            "summary, reports",
            ["test-public"],
        ),
        markdown(
            "## Decision memo\n\nChoose a threshold for high missed-failure cost and limited inspection capacity. Report expected false alarms and misses in this evaluation sample, one failure pattern to inspect, and why PR-AUC must be compared with prevalence. Do not describe the score as factory validation or causal evidence."
        ),
        markdown(
            "**Instructor note.** Accept more than one threshold when the consequence argument and counts agree. Penalise threshold selection on the final test, not a non-default threshold itself.",
            ["instructor-only"],
        ),
    ]
    nbformat.write(notebook(meta, cells), OUTPUT / "metrics-errors.ipynb")


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    build_tabular()
    build_quality()
    build_eda()
    build_safe_pipeline()
    build_metrics()
    print("Built five P0 foundation notebooks")


if __name__ == "__main__":
    main()
