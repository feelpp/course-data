#!/usr/bin/env python3
"""Build deterministic canonical notebooks for the P1 analytical core."""

from __future__ import annotations

from pathlib import Path

import nbformat

from tools.build_foundation_notebooks import (
    LOCATOR,
    code,
    deterministic_cell_id,
    markdown,
    notebook,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "notebooks" / "instructor" / "analytical"


def write_notebook(filename: str, content: nbformat.NotebookNode) -> None:
    for index, cell in enumerate(content.cells):
        cell["id"] = deterministic_cell_id(f"analytical/{filename}", index)
    nbformat.write(content, OUTPUT / filename)


def metadata(concepts: list[str], outcomes: list[str], difficulty: str, duration: int) -> dict:
    return {
        "assessed": True,
        "concept_ids": concepts,
        "difficulty": difficulty,
        "duration_minutes": duration,
        "execution_profile": "full",
        "language": "en",
        "outcomes": outcomes,
        "prerequisites": ["P0 foundation path"],
        "priority": "P1",
    }


def build_linear() -> None:
    meta = metadata(
        ["DP-LIN-01", "DP-PROB-01", "DP-NUM-01", "DP-MET-01"],
        ["LO6", "LO7", "LO8"],
        "D2",
        100,
    )
    cells = [
        markdown(
            "# Stable linear regression and probability\n\n**P1 Core · D2 Independent · 100 minutes**"
        ),
        code(
            "import numpy as np\nfrom sklearn.linear_model import Ridge\nfrom sklearn.metrics import mean_absolute_error, mean_squared_error",
            ["setup"],
        ),
        code(
            "rng = np.random.default_rng(20260718)\n"
            "x1 = rng.normal(size=250)\n"
            "x2 = x1 + 1e-7 * rng.normal(size=250)\n"
            "X = np.column_stack([np.ones(len(x1)), x1, x2])\n"
            "y = 1.5 + 3.0*x1 - 2.0*x2 + 0.1*rng.normal(size=len(x1))\n"
            "condition = np.linalg.cond(X)\ncondition",
            ["setup"],
        ),
        markdown(
            "## Task\n\nFit coefficients without an explicit inverse and return coefficients, predictions, residuals, MAE, RMSE, and Gaussian negative log-likelihood up to an additive constant."
        ),
        code(
            "def stable_fit(X: np.ndarray, y: np.ndarray) -> dict:\n"
            "    beta, _, rank, singular = np.linalg.lstsq(X, y, rcond=None)\n"
            "    prediction = X @ beta\n"
            "    residual = y - prediction\n"
            "    variance = np.mean(residual**2)\n"
            "    return {'beta': beta, 'prediction': prediction, 'residual': residual,\n"
            "            'rank': int(rank), 'singular': singular,\n"
            "            'mae': mean_absolute_error(y, prediction),\n"
            "            'rmse': mean_squared_error(y, prediction)**0.5,\n"
            "            'gaussian_nll': 0.5*len(y)*np.log(variance) + 0.5*np.sum(residual**2)/variance}",
            ["solution"],
            "def stable_fit(X: np.ndarray, y: np.ndarray) -> dict:\n"
            "    # TODO: use lstsq/QR/SVD, then compute residual and likelihood evidence.\n"
            "    raise NotImplementedError\n",
        ),
        code(
            "result = stable_fit(X, y)\n"
            "assert condition > 1e6\n"
            "assert result['rank'] == X.shape[1]\n"
            "assert result['rmse'] < 0.12\n"
            "ridge = Ridge(alpha=1.0, fit_intercept=False).fit(X, y)\n"
            "assert np.linalg.norm(ridge.coef_) < np.linalg.norm(result['beta'])\n"
            "{k: result[k] for k in ('rank','mae','rmse','gaussian_nll')}",
            ["test-public"],
        ),
        markdown(
            "## Transfer\n\nUse a chronological air-quality holdout. Compare stable least squares and Ridge, inspect residuals by time/prediction, and state which Gaussian and independence assumptions fail."
        ),
    ]
    write_notebook("linear-probabilistic.ipynb", notebook(meta, cells))


def build_classification() -> None:
    meta = metadata(
        ["DP-CLS-01", "DP-PROB-01", "DP-NUM-01", "DP-MET-02", "DP-THR-01"],
        ["LO6", "LO7"],
        "D3",
        100,
    )
    cells = [
        markdown("# Stable classification losses\n\n**P1 Core · D3 Synthesis · 100 minutes**"),
        code("import numpy as np\nfrom scipy.special import logsumexp\n" + LOCATOR, ["setup"]),
        markdown(
            "## Task\n\nImplement stable row-wise softmax and mean cross-entropy from integer labels. Verify shift invariance and extreme logits."
        ),
        code(
            "def stable_softmax(logits: np.ndarray) -> np.ndarray:\n"
            "    shifted = logits - logits.max(axis=1, keepdims=True)\n"
            "    exp = np.exp(shifted)\n"
            "    return exp / exp.sum(axis=1, keepdims=True)\n\n"
            "def cross_entropy(logits: np.ndarray, labels: np.ndarray) -> float:\n"
            "    log_normaliser = logsumexp(logits, axis=1)\n"
            "    return float(np.mean(log_normaliser - logits[np.arange(len(labels)), labels]))",
            ["solution"],
            "def stable_softmax(logits: np.ndarray) -> np.ndarray:\n"
            "    # TODO: subtract a row constant before exponentiating.\n"
            "    raise NotImplementedError\n\n"
            "def cross_entropy(logits: np.ndarray, labels: np.ndarray) -> float:\n"
            "    # TODO: compute categorical negative log-likelihood stably.\n"
            "    raise NotImplementedError\n",
        ),
        code(
            "logits = np.array([[1000., 1001., 999.], [-1000., -1001., -999.]])\n"
            "labels = np.array([1, 2])\n"
            "probability = stable_softmax(logits)\n"
            "loss = cross_entropy(logits, labels)\n"
            "assert np.isfinite(probability).all() and np.isfinite(loss)\n"
            "assert np.allclose(probability.sum(axis=1), 1.0)\n"
            "assert np.allclose(probability, stable_softmax(logits + 12345.))\n"
            "assert loss < 1.0\n"
            "probability, loss",
            ["test-public"],
        ),
        markdown(
            "## Dry Bean guided fit\n\nLoad the teaching CSV, stratify a subset, scale inside a pipeline, fit multinomial logistic regression, and report log loss plus per-class confusion. Class labels must not enter preprocessing features."
        ),
        code(
            "import pandas as pd\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.metrics import log_loss\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.pipeline import make_pipeline\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "path = locate('datasets/teaching/dry-bean/observations.csv', 'observations.csv')\n"
            "beans = pd.read_csv(path).groupby('Class', group_keys=False).sample(n=300, random_state=7)\n"
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    beans.drop(columns='Class'), beans['Class'], test_size=0.25, random_state=7, stratify=beans['Class'])\n"
            "model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(X_train, y_train)\n"
            "loss_library = log_loss(y_test, model.predict_proba(X_test), labels=model.classes_)\n"
            "assert loss_library < 0.6\nloss_library",
            ["demo", "test-public"],
        ),
        markdown(
            "## Transfer\n\nOn an imbalanced three-class oracle, compare macro-F1, per-class recall and log loss; explain how loss can change without changing argmax decisions."
        ),
    ]
    write_notebook("classification-losses.ipynb", notebook(meta, cells))


def build_regularisation() -> None:
    meta = metadata(
        ["DP-REG-01", "DP-GEN-01", "DP-CV-01", "DP-NUM-01"],
        ["LO5", "LO6", "LO7"],
        "D3",
        100,
    )
    cells = [
        markdown("# Regularisation and generalisation\n\n**P1 Core · D3 Synthesis · 100 minutes**"),
        code(
            "import numpy as np\n"
            "from sklearn.linear_model import LassoCV, RidgeCV\n"
            "from sklearn.metrics import mean_squared_error\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.pipeline import make_pipeline\n"
            "from sklearn.preprocessing import PolynomialFeatures, StandardScaler",
            ["setup"],
        ),
        code(
            "rng = np.random.default_rng(19)\n"
            "x = rng.uniform(-2, 2, size=(240, 1))\n"
            "y = 1 - 2*x[:,0] + 0.8*x[:,0]**2 + rng.normal(scale=1.0, size=len(x))\n"
            "X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=19)",
            ["setup"],
        ),
        markdown(
            "## Task\n\nFit degree-12 polynomial Ridge and Lasso pipelines. Scaling and penalty selection must occur inside the fitted workflow."
        ),
        code(
            "def regularised_models():\n"
            "    ridge = make_pipeline(PolynomialFeatures(12, include_bias=False), StandardScaler(),\n"
            "                          RidgeCV(alphas=np.logspace(-4, 3, 16), cv=5))\n"
            "    lasso = make_pipeline(PolynomialFeatures(12, include_bias=False), StandardScaler(),\n"
            "                          LassoCV(alphas=np.logspace(-4, 0, 16), cv=5, max_iter=20000,\n"
            "                                  random_state=19))\n"
            "    return ridge, lasso",
            ["solution"],
            "def regularised_models():\n"
            "    # TODO: polynomial features, scaling, and penalty selection inside pipelines.\n"
            "    raise NotImplementedError\n",
        ),
        code(
            "ridge, lasso = regularised_models()\n"
            "ridge.fit(X_train, y_train); lasso.fit(X_train, y_train)\n"
            "ridge_rmse = mean_squared_error(y_test, ridge.predict(X_test))**0.5\n"
            "lasso_rmse = mean_squared_error(y_test, lasso.predict(X_test))**0.5\n"
            "lasso_coef = lasso.named_steps['lassocv'].coef_\n"
            "assert ridge_rmse < 1.5 and lasso_rmse < 1.5\n"
            "assert np.count_nonzero(lasso_coef) < len(lasso_coef)\n"
            "{'ridge_rmse': ridge_rmse, 'lasso_rmse': lasso_rmse,\n"
            " 'lasso_nonzero': int(np.count_nonzero(lasso_coef))}",
            ["test-public"],
        ),
        markdown(
            "## Transfer\n\nRepeat across sample seeds, report coefficient-selection stability and a learning curve, and explain why sparse predictive coefficients are not causal discoveries."
        ),
    ]
    write_notebook("regularisation-generalisation.ipynb", notebook(meta, cells))


def build_selection() -> None:
    meta = metadata(
        ["DP-CV-01", "DP-SEARCH-01", "DP-FEAT-01", "DP-EVAL-02", "DP-PIPE-01"],
        ["LO5", "LO6", "LO7", "LO9"],
        "D3",
        100,
    )
    cells = [
        markdown("# Cross-validation and search\n\n**P1 Core · D3 Synthesis · 100 minutes**"),
        code(
            "import numpy as np\nimport pandas as pd\n"
            "from sklearn.compose import ColumnTransformer\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.model_selection import GroupKFold, StratifiedKFold, cross_val_score\n"
            "from sklearn.pipeline import Pipeline\nfrom sklearn.preprocessing import OneHotEncoder, StandardScaler",
            ["setup"],
        ),
        code(
            "rng = np.random.default_rng(23)\n"
            "groups = np.repeat(np.arange(30), 20)\n"
            "group_target = rng.integers(0, 2, size=30)\n"
            "y = group_target[groups]\n"
            "frame = pd.DataFrame({'group': groups.astype(str), 'weak_signal': y + rng.normal(scale=2.5, size=len(y))})",
            ["setup"],
        ),
        markdown(
            "## Task\n\nCompare ordinary stratified folds with group-held-out folds. The group identity is deliberately learnable in random-row folds and unseen in group folds."
        ),
        code(
            "def compare_folds(frame, y, groups):\n"
            "    preprocess = ColumnTransformer([\n"
            "        ('group', OneHotEncoder(handle_unknown='ignore'), ['group']),\n"
            "        ('signal', StandardScaler(), ['weak_signal'])])\n"
            "    model = Pipeline([('preprocess', preprocess), ('model', LogisticRegression(max_iter=1000))])\n"
            "    random_cv = StratifiedKFold(5, shuffle=True, random_state=23)\n"
            "    group_cv = GroupKFold(5)\n"
            "    random_score = cross_val_score(model, frame, y, cv=random_cv, scoring='accuracy')\n"
            "    group_score = cross_val_score(model, frame, y, groups=groups, cv=group_cv, scoring='accuracy')\n"
            "    return random_score, group_score",
            ["solution"],
            "def compare_folds(frame, y, groups):\n"
            "    # TODO: one full pipeline; compare random-row and group-held-out folds.\n"
            "    raise NotImplementedError\n",
        ),
        code(
            "random_score, group_score = compare_folds(frame, y, groups)\n"
            "assert random_score.mean() > group_score.mean() + 0.15\n"
            "{'random_mean': random_score.mean(), 'group_mean': group_score.mean(),\n"
            " 'group_spread': group_score.std()}",
            ["test-public"],
        ),
        markdown(
            "## Transfer\n\nUse chronological air-quality validation, place feature selection inside the pipeline, run a fixed-budget random search, and preserve one final time block."
        ),
    ]
    write_notebook("model-selection.ipynb", notebook(meta, cells))


def build_trees() -> None:
    meta = metadata(
        ["DP-TREE-01", "DP-ENS-01", "DP-ENS-02", "DP-CV-01", "DP-INT-01"],
        ["LO6", "LO7", "LO10"],
        "D2",
        100,
    )
    cells = [
        markdown("# Trees, forests, and boosting\n\n**P1 Core · D2 Independent · 100 minutes**"),
        code(
            "import pandas as pd\n"
            "from sklearn.compose import ColumnTransformer\nfrom sklearn.dummy import DummyClassifier\n"
            "from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier\n"
            "from sklearn.metrics import average_precision_score\nfrom sklearn.model_selection import train_test_split\n"
            "from sklearn.pipeline import Pipeline\nfrom sklearn.preprocessing import OneHotEncoder\n"
            "from sklearn.tree import DecisionTreeClassifier\n" + LOCATOR,
            ["setup"],
        ),
        code(
            "path = locate('datasets/teaching/predictive-maintenance/observations.csv', 'observations.csv')\n"
            "data = pd.read_csv(path)\n"
            "features = ['Type','Air temperature [K]','Process temperature [K]',\n"
            "            'Rotational speed [rpm]','Torque [Nm]','Tool wear [min]']\n"
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    data[features], data['Machine failure'], test_size=.25, random_state=29, stratify=data['Machine failure'])\n"
            "pre = ColumnTransformer([('type', OneHotEncoder(handle_unknown='ignore', sparse_output=False), ['Type'])],\n"
            "                        remainder='passthrough')",
            ["setup"],
        ),
        markdown(
            "## Task\n\nFit a controlled tree, OOB random forest, and histogram boosting model under fixed budgets. Return protected-test PR-AUC."
        ),
        code(
            "def compare_models():\n"
            "    estimators = {\n"
            "        'tree': DecisionTreeClassifier(max_depth=5, min_samples_leaf=20, class_weight='balanced', random_state=29),\n"
            "        'forest': RandomForestClassifier(n_estimators=120, min_samples_leaf=5, class_weight='balanced',\n"
            "                                         oob_score=True, n_jobs=1, random_state=29),\n"
            "        'boosting': HistGradientBoostingClassifier(max_iter=100, max_leaf_nodes=15, learning_rate=.08,\n"
            "                                                   class_weight='balanced', random_state=29),\n"
            "    }\n"
            "    scores = {}\n"
            "    fitted = {}\n"
            "    for name, estimator in estimators.items():\n"
            "        pipeline = Pipeline([('preprocess', pre), ('model', estimator)]).fit(X_train, y_train)\n"
            "        scores[name] = average_precision_score(y_test, pipeline.predict_proba(X_test)[:,1])\n"
            "        fitted[name] = pipeline\n"
            "    return scores, fitted",
            ["solution"],
            "def compare_models():\n"
            "    # TODO: controlled tree, OOB forest, and fixed-budget boosting on the same split.\n"
            "    raise NotImplementedError\n",
        ),
        code(
            "scores, fitted = compare_models()\n"
            "dummy = DummyClassifier(strategy='prior').fit(X_train, y_train)\n"
            "dummy_ap = average_precision_score(y_test, dummy.predict_proba(X_test)[:,1])\n"
            "assert max(scores.values()) > dummy_ap\n"
            "assert 0 < fitted['forest'].named_steps['model'].oob_score_ < 1\n"
            "{'dummy': dummy_ap, **scores}",
            ["test-public"],
        ),
        markdown(
            "## Transfer\n\nPerturb the sample seed, compare tree/importance instability, relate OOB to test evidence, and explain why predictive importance is non-causal."
        ),
    ]
    write_notebook("tree-ensembles.ipynb", notebook(meta, cells))


def build_pca_clustering() -> None:
    meta = metadata(
        ["DP-PCA-01", "DP-CLU-01", "DP-CLU-02", "DP-CLU-03", "DP-NUM-01"],
        ["LO6", "LO7", "LO8"],
        "D3",
        110,
    )
    cells = [
        markdown("# PCA and clustering\n\n**P1 Core · D3 Synthesis · 110 minutes**"),
        code(
            "import pandas as pd\n"
            "from sklearn.cluster import AgglomerativeClustering, DBSCAN, KMeans\n"
            "from sklearn.decomposition import PCA\nfrom sklearn.metrics import adjusted_rand_score, silhouette_score\n"
            "from sklearn.pipeline import make_pipeline\nfrom sklearn.preprocessing import StandardScaler\n"
            + LOCATOR,
            ["setup"],
        ),
        code(
            "path = locate('datasets/teaching/dry-bean/observations.csv', 'observations.csv')\n"
            "beans = pd.read_csv(path).groupby('Class', group_keys=False).sample(n=220, random_state=31)\n"
            "X = beans.drop(columns='Class'); labels = beans['Class']",
            ["setup"],
        ),
        markdown(
            "## Task\n\nScale features, retain at least 90% PCA variance, fit seven-cluster k-means, and report internal plus post-hoc stability evidence. `Class` cannot enter fitting."
        ),
        code(
            "def pca_cluster(X: pd.DataFrame) -> dict:\n"
            "    transform = make_pipeline(StandardScaler(), PCA(n_components=.90, random_state=31))\n"
            "    reduced = transform.fit_transform(X)\n"
            "    first = KMeans(7, n_init=20, random_state=31).fit_predict(reduced)\n"
            "    second = KMeans(7, n_init=20, random_state=32).fit_predict(reduced)\n"
            "    pca = transform.named_steps['pca']\n"
            "    return {'reduced': reduced, 'first': first, 'second': second,\n"
            "            'variance': float(pca.explained_variance_ratio_.sum()),\n"
            "            'silhouette': silhouette_score(reduced, first),\n"
            "            'seed_stability': adjusted_rand_score(first, second)}",
            ["solution"],
            "def pca_cluster(X: pd.DataFrame) -> dict:\n"
            "    # TODO: scale, fit PCA without Class, cluster twice, and report variance/stability.\n"
            "    raise NotImplementedError\n",
        ),
        code(
            "result = pca_cluster(X)\n"
            "assert result['variance'] >= .90\n"
            "assert result['reduced'].shape[1] < X.shape[1]\n"
            "assert result['seed_stability'] > .85\n"
            "posthoc_ari = adjusted_rand_score(labels, result['first'])\n"
            "{'variance': result['variance'], 'silhouette': result['silhouette'],\n"
            " 'seed_stability': result['seed_stability'], 'class_ari_posthoc': posthoc_ari}",
            ["test-public"],
        ),
        markdown(
            "## Transfer\n\nChallenge k-means on anisotropic/noisy/varying-density oracles; compare hierarchical clustering and DBSCAN, bootstrap stability, and domain interpretation."
        ),
    ]
    write_notebook("pca-clustering.ipynb", notebook(meta, cells))


def build_performance() -> None:
    meta = metadata(
        ["DP-PERF-01", "DP-FMT-01", "DP-SQL-01", "DP-ARR-01"],
        ["LO3", "LO8", "LO9"],
        "D2",
        100,
    )
    cells = [
        markdown("# Columnar performance\n\n**P1 Core · D2 Independent · 100 minutes**"),
        code(
            "import tempfile\nfrom pathlib import Path\nimport duckdb\nimport pandas as pd\n"
            + LOCATOR,
            ["setup"],
        ),
        code(
            "path = locate('datasets/teaching/air-quality/observations.csv', 'observations.csv')\n"
            "source = pd.read_csv(path)\n"
            "expanded = pd.concat([source.assign(replicate=i) for i in range(100)], ignore_index=True)\n"
            "expanded['observation_id'] = range(len(expanded))\nexpanded.shape",
            ["setup"],
        ),
        markdown(
            "## Task\n\nWrite CSV/Parquet, use projected Parquet reads and DuckDB filtered aggregation, and verify result equality. Do not assert that one noisy timing must be faster."
        ),
        code(
            "def columnar_evidence(frame: pd.DataFrame) -> dict:\n"
            "    with tempfile.TemporaryDirectory() as directory:\n"
            "        directory = Path(directory)\n"
            "        csv_path = directory/'air.csv'; parquet_path = directory/'air.parquet'\n"
            "        frame.to_csv(csv_path, index=False); frame.to_parquet(parquet_path, index=False)\n"
            "        projected = pd.read_parquet(parquet_path, columns=['station','PM2.5','replicate'])\n"
            "        pandas_result = (projected.query(\"station == 'Dingling'\")\n"
            "                         .groupby('replicate')['PM2.5'].mean().sort_index())\n"
            '        query = "SELECT replicate, avg(\\"PM2.5\\") AS mean_pm25 FROM read_parquet(?) '
            "                WHERE station='Dingling' GROUP BY replicate ORDER BY replicate\"\n"
            "        duck = duckdb.execute(query, [str(parquet_path)]).fetchdf().set_index('replicate')['mean_pm25']\n"
            "        return {'rows': len(frame), 'csv_bytes': csv_path.stat().st_size,\n"
            "                'parquet_bytes': parquet_path.stat().st_size,\n"
            "                'selected_columns': list(projected.columns),\n"
            "                'equal': bool(pd.Series(pandas_result).round(10).equals(duck.round(10)))}",
            ["solution"],
            "def columnar_evidence(frame: pd.DataFrame) -> dict:\n"
            "    # TODO: CSV/Parquet artifacts, projected read, pushed-down query, equality evidence.\n"
            "    raise NotImplementedError\n",
        ),
        code(
            "evidence = columnar_evidence(expanded)\n"
            "assert evidence['rows'] == 100_800\n"
            "assert evidence['parquet_bytes'] < evidence['csv_bytes']\n"
            "assert evidence['selected_columns'] == ['station','PM2.5','replicate']\n"
            "assert evidence['equal']\n"
            "evidence",
            ["test-public"],
        ),
        markdown(
            "## Transfer\n\nUnder a fixed memory budget, compare full CSV materialisation, projected Parquet, and a filtered aggregate. Explain chunking and why distribution overhead may dominate."
        ),
    ]
    write_notebook("performance-columnar.ipynb", notebook(meta, cells))


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    build_linear()
    build_classification()
    build_regularisation()
    build_selection()
    build_trees()
    build_pca_clustering()
    build_performance()
    print("Built seven P1 analytical notebooks")


if __name__ == "__main__":
    main()
