"""Extract four declared windows from the pinned Beijing archive; no network."""

from __future__ import annotations

import hashlib
from pathlib import Path
from zipfile import ZipFile

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[3]
DESTINATION = ROOT / "datasets/teaching/air-quality-seasonal"


def main() -> None:
    snapshot = ROOT / "datasets/snapshots/uci-501/source.zip"
    source = yaml.safe_load(snapshot.with_name("SOURCE.yml").read_text())
    assert hashlib.sha256(snapshot.read_bytes()).hexdigest() == source["snapshot_sha256"]
    tables = []
    with ZipFile(snapshot) as archive:
        for station in ("Aotizhongxin", "Changping", "Dingling"):
            member = f"PRSA_Data_20130301-20170228/PRSA_Data_{station}_20130301-20170228.csv"
            frame = pd.read_csv(archive.open(member))
            selected = frame.loc[
                (frame.year == 2013) & frame.month.isin([3, 6, 9, 12]) & (frame.day <= 14)
            ].rename(columns={"No": "source_row"})
            tables.append(selected)
    data = pd.concat(tables, ignore_index=True)
    assert data.shape == (4032, 18)
    DESTINATION.mkdir(parents=True, exist_ok=True)
    path = DESTINATION / "observations.csv"
    data.to_csv(path, index=False, lineterminator="\n")
    manifest = {
        "schema_version": 1,
        "source_id": "uci-501",
        "licence": "CC-BY-4.0",
        "generated_by": "teaching/sessions/multivariate/build_seasonal_data.py",
        "snapshot_sha256": source["snapshot_sha256"],
        "note": "Days 1–14 of March, June, September, December 2013 at three stations; "
        "unmodified values, selected windows, not a seasonal climatology.",
        "files": [
            {
                "path": path.name,
                "rows": len(data),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "size_bytes": path.stat().st_size,
            }
        ],
    }
    (DESTINATION / "MANIFEST.yml").write_text(yaml.safe_dump(manifest, sort_keys=False))
    print(f"Prepared {len(data)} original station-hours in {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
