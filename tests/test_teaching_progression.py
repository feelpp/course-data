import re
from copy import deepcopy
from pathlib import Path

import numpy as np
import yaml
from sklearn.preprocessing import StandardScaler

from tools.validate_repository import validate_contact_time

ROOT = Path(__file__).resolve().parents[1]


def test_contact_time_does_not_double_count_controls_or_distributed_practice():
    curriculum = yaml.safe_load((ROOT / "curriculum.yml").read_text())
    errors = []
    validate_contact_time(curriculum, errors)
    assert not errors
    oversized = deepcopy(curriculum)
    oversized["schedule"][7]["contact_plan"].append({"label": "extra lab", "minutes": 50})
    validate_contact_time(oversized, errors)
    assert any("Block 8" in error for error in errors)
    duplicated = deepcopy(curriculum)
    duplicated["schedule"][13]["contact_plan"][1]["activity"] = "E14"
    errors = []
    validate_contact_time(duplicated, errors)
    assert any("E14" in error for error in errors)


def test_regularisation_example_fits_scaling_only_on_training_folds(monkeypatch):
    source = (
        ROOT / "docs/course/modules/ROOT/pages/analytical/regularisation-generalisation.adoc"
    ).read_text()
    code = re.search(
        r"\[#regularisation-summary-table\][\s\S]*?\n----\n([\s\S]*?)\n----", source
    ).group(1)
    fitted_rows = []
    original_fit = StandardScaler.fit

    def record_fit(self, X, y=None, **kwargs):
        # The first polynomial column preserves the unique original x values.
        fitted_rows.append(frozenset(np.asarray(X)[:, 0]))
        return original_fit(self, X, y, **kwargs)

    monkeypatch.setattr(StandardScaler, "fit", record_fit)
    scope = {}
    exec(compile(code, "regularisation-example", "exec"), scope)
    train = scope["X_train"]
    full_training = frozenset(train[:, 0])
    held_out = frozenset(scope["X_test"][:, 0])
    fold_training = {
        frozenset(train[indices, 0])
        for indices, _ in scope["selection_cv"].split(train, scope["y_train"])
    }
    assert fold_training <= set(fitted_rows)
    assert full_training in fitted_rows
    assert all(rows in fold_training or rows == full_training for rows in fitted_rows)
    assert all(rows.isdisjoint(held_out) for rows in fitted_rows)
