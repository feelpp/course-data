from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def test_air_quality_slice_preserves_identity_and_scope() -> None:
    data = pd.read_csv(ROOT / "datasets/teaching/air-quality/observations.csv")
    key = ["station", "year", "month", "day", "hour"]
    assert len(data) == 3 * 14 * 24
    assert data[key].notna().all().all()
    assert not data.duplicated(key).any()
    assert set(data["station"]) == {"Aotizhongxin", "Changping", "Dingling"}
    assert set(data["year"]) == {2013}
    assert set(data["month"]) == {3}


def test_predictive_maintenance_feature_roles_flag_leakage() -> None:
    data = pd.read_csv(ROOT / "datasets/teaching/predictive-maintenance/observations.csv")
    failure_modes = ["TWF", "HDF", "PWF", "OSF", "RNF"]
    assert len(data) == 10_000
    assert set(data["Machine failure"].unique()) <= {0, 1}
    assert all(set(data[column].unique()) <= {0, 1} for column in failure_modes)
    direct_modes = ["TWF", "HDF", "PWF", "OSF"]
    assert all((data["Machine failure"] >= data[column]).all() for column in direct_modes)
    any_failure_mode = data[failure_modes].max(axis=1)
    covered_failures = any_failure_mode[data["Machine failure"].eq(1)].mean()
    assert covered_failures > 0.95
