import pytest

from src.analysis import read_observations


def test_toy_oracle_preserves_identity_and_values(tmp_path):
    data = tmp_path / "toy.csv"
    data.write_text("observation_id,value\na,1.5\nb,2.0\n")
    assert read_observations(data) == [
        {"observation_id": "a", "value": 1.5},
        {"observation_id": "b", "value": 2.0},
    ]


@pytest.mark.parametrize("rows", ["a,1\na,2\n", ",1\n", "a,nan\n", "a,inf\n"])
def test_rejects_invalid_identity_or_measurement(tmp_path, rows):
    data = tmp_path / "toy.csv"
    data.write_text("observation_id,value\n" + rows)
    with pytest.raises(ValueError):
        read_observations(data)
