#!/usr/bin/env python3
"""Build deterministic, licensed teaching tables from reviewed snapshots."""

from __future__ import annotations

import hashlib
import io
import zipfile
from pathlib import Path

import pandas as pd
import yaml
from scipy.io import arff

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOTS = ROOT / "datasets" / "snapshots"
OUTPUT = ROOT / "datasets" / "teaching"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_manifest(directory: Path, source_id: str, outputs: list[Path], note: str) -> None:
    manifest = {
        "schema_version": 1,
        "source_id": source_id,
        "licence": "CC-BY-4.0",
        "generated_by": "tools/build_teaching_data.py",
        "note": note,
        "files": [
            {
                "path": path.name,
                "rows": len(pd.read_csv(path)),
                "sha256": digest(path),
                "size_bytes": path.stat().st_size,
            }
            for path in outputs
        ],
    }
    (directory / "MANIFEST.yml").write_text(
        yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8"
    )


def build_air_quality() -> None:
    destination = OUTPUT / "air-quality"
    destination.mkdir(parents=True, exist_ok=True)
    archive_path = SNAPSHOTS / "uci-501" / "source.zip"
    stations = ["Aotizhongxin", "Changping", "Dingling"]
    tables: list[pd.DataFrame] = []
    registry: list[dict[str, str | int]] = []
    with zipfile.ZipFile(archive_path) as archive:
        for station in stations:
            member = f"PRSA_Data_20130301-20170228/PRSA_Data_{station}_20130301-20170228.csv"
            frame = pd.read_csv(archive.open(member))
            selected = frame.query("year == 2013 and month == 3 and day <= 14").copy()
            selected = selected.rename(columns={"No": "source_row"})
            tables.append(selected)
            registry.append(
                {
                    "station": station,
                    "source_file": Path(member).name,
                    "upstream_rows": len(frame),
                }
            )
    observations = pd.concat(tables, ignore_index=True)
    observations_path = destination / "observations.csv"
    stations_path = destination / "stations.csv"
    observations.to_csv(observations_path, index=False, lineterminator="\n")
    pd.DataFrame(registry).to_csv(stations_path, index=False, lineterminator="\n")
    write_manifest(
        destination,
        "uci-501",
        [observations_path, stations_path],
        "First fourteen days of March 2013 for three stations; values are unmodified.",
    )


def build_predictive_maintenance() -> None:
    destination = OUTPUT / "predictive-maintenance"
    destination.mkdir(parents=True, exist_ok=True)
    archive_path = SNAPSHOTS / "uci-601" / "source.zip"
    with zipfile.ZipFile(archive_path) as archive:
        source = archive.read("ai4i2020.csv")
    frame = pd.read_csv(io.BytesIO(source))
    output_path = destination / "observations.csv"
    frame.to_csv(output_path, index=False, lineterminator="\n")
    write_manifest(
        destination,
        "uci-601",
        [output_path],
        "Complete upstream synthetic table; failure-mode columns are target-derived leakage.",
    )


def build_dry_bean() -> None:
    destination = OUTPUT / "dry-bean"
    destination.mkdir(parents=True, exist_ok=True)
    archive_path = SNAPSHOTS / "uci-602" / "source.zip"
    with zipfile.ZipFile(archive_path) as archive:
        source = archive.read("DryBeanDataset/Dry_Bean_Dataset.arff")
    records, _ = arff.loadarff(io.StringIO(source.decode("utf-8")))
    frame = pd.DataFrame(records)
    frame["Class"] = frame["Class"].str.decode("utf-8")
    output_path = destination / "observations.csv"
    frame.to_csv(output_path, index=False, lineterminator="\n")
    write_manifest(
        destination,
        "uci-602",
        [output_path],
        "Complete upstream feature table converted losslessly from ARFF to UTF-8 CSV.",
    )


def main() -> None:
    build_air_quality()
    build_predictive_maintenance()
    build_dry_bean()
    print("Built reviewed teaching tables for uci-501, uci-601, and uci-602")


if __name__ == "__main__":
    main()
