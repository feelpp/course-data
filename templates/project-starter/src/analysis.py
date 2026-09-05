"""A minimal toy input contract; replace with your approved scientific analysis."""

import csv
import math
from pathlib import Path


def read_observations(path: Path) -> list[dict]:
    """Read unique, nonempty IDs and finite numeric values without dropping rows."""
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["observation_id", "value"]:
            raise ValueError("Expected observation_id,value schema")
        rows = list(reader)
    identifiers = [row["observation_id"] for row in rows]
    if any(not identifier for identifier in identifiers) or len(set(identifiers)) != len(rows):
        raise ValueError("Observation IDs must be nonempty and unique")
    for row in rows:
        row["value"] = float(row["value"])
        if not math.isfinite(row["value"]):
            raise ValueError("Values must be finite")
    return rows


if __name__ == "__main__":
    data = Path(__file__).resolve().parents[1] / "data/toy.csv"
    print(f"Validated {len(read_observations(data))} toy observations; add your analysis next.")
