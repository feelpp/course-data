"""Compute checked teacher references for the native Typst handouts.

No computed Beijing result is inserted into the student sheet or class slides.
"""

from __future__ import annotations

import csv
import json
import math
import statistics as stats
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "build/teaching/20261020"
STAGE = WORK / "typst"
with (ROOT / "datasets/teaching/air-quality/observations.csv").open() as stream:
    data = list(csv.DictReader(stream))
assert len(data) == 1008


def value(row, name):
    try:
        result = float(row[name])
        return result if math.isfinite(result) else None
    except (ValueError, TypeError):
        return None


def pair_result(left, right):
    pairs = [(value(row, left), value(row, right)) for row in data]
    pairs = [(x, y) for x, y in pairs if x is not None and y is not None]
    x, y = zip(*pairs, strict=False)
    s_xy = stats.covariance(x, y)
    r_xy = stats.correlation(x, y)
    np.testing.assert_allclose(s_xy, np.cov(x, y, ddof=1)[0, 1])
    np.testing.assert_allclose(r_xy, np.corrcoef(x, y)[0, 1])
    return {"pair": f"{left} / {right}", "n": len(pairs), "covariance": s_xy, "r": r_xy}


train = [value(row, "PM2.5") for row in data if int(row["day"]) <= 10]
valid = [value(row, "PM2.5") for row in data if 11 <= int(row["day"]) <= 12]
reserved = [row for row in data if int(row["day"]) >= 13]
baseline = stats.median([x for x in train if x is not None])
validation_targets = [x for x in valid if x is not None]
mae = stats.mean(abs(x - baseline) for x in validation_targets)
assert (len(train), len(valid), len(reserved)) == (720, 144, 144)
assert baseline == 56.5 and math.isclose(mae, 73.09027777777777)
columns = ["PM2.5", "PM10", "WSPM"]
common = [[value(row, name) for name in columns] for row in data]
X = np.array([row for row in common if all(v is not None for v in row)])
assert X.shape == (1002, 3)
C = X - X.mean(axis=0)
S = C.T @ C / (len(X) - 1)
np.testing.assert_allclose(S, np.cov(X, rowvar=False, ddof=1))
results = {
    "train_rows": len(train),
    "validation_rows": len(valid),
    "reserved_rows": len(reserved),
    "baseline": baseline,
    "validation_mae": mae,
    "pairs": [
        pair_result(a, b)
        for a, b in [("PM2.5", "PM10"), ("TEMP", "DEWP"), ("TEMP", "PRES"), ("PM2.5", "WSPM")]
    ],
    "common_n": len(X),
    "S": S.tolist(),
}
STAGE.mkdir(parents=True, exist_ok=True)
(STAGE / "teacher.json").write_text(json.dumps(results, indent=2))
(WORK / "teacher-results.json").write_text(json.dumps(results, indent=2))
print("Verified teacher references for the Typst guide")
