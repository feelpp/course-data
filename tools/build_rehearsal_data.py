#!/usr/bin/env python3
"""Create original, deterministic synthetic data for public assessment rehearsal."""

from __future__ import annotations

import csv
import hashlib
import random
from datetime import UTC, datetime, timedelta
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "datasets/teaching/rehearsal"


def build(destination: Path = DESTINATION) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    rng = random.Random(20260905)
    origin = datetime(2026, 1, 1, tzinfo=UTC)
    machines = [{"machine_id": f"M{i:02d}", "family": ["A", "B", "C"][i % 3]} for i in range(20)]
    cycles = []
    for i in range(120):
        temperature_c = round(rng.gauss(52, 11), 2)
        vibration = round(rng.uniform(0.1, 4.5), 3)
        inspection = int(temperature_c + 7 * vibration + rng.gauss(0, 8) > 76)
        unit = "K" if i % 11 == 0 else "degC"
        cycles.append(
            {
                "cycle_id": f"C{i:03d}",
                "machine_id": machines[i // 6]["machine_id"],
                "recorded_at": (origin + timedelta(hours=i)).isoformat(),
                "temperature": round(temperature_c + (273.15 if unit == "K" else 0), 2),
                "temperature_unit": unit,
                "vibration_mm_s": "" if i % 13 == 0 else vibration,
                "requires_inspection": inspection,
                "inspection_completed": inspection,
            }
        )
    cycles[17]["temperature"] = -999
    cycles.append(cycles[8].copy())
    sites = [{"site_id": f"S{i:02d}", "catchment": ["rural", "urban"][i % 2]} for i in range(15)]
    samples = []
    for i in range(120):
        concentration = round(rng.uniform(0.01, 0.19), 4)
        temperature = round(rng.gauss(16, 4), 2)
        review = int(concentration + 0.002 * temperature + rng.gauss(0, 0.025) > 0.145)
        unit = "ug/L" if i % 9 == 0 else "mg/L"
        samples.append(
            {
                "sample_id": f"E{i:03d}",
                "site_id": sites[i // 8]["site_id"],
                "collected_at": (origin + timedelta(hours=3 * i)).isoformat(),
                "instrument_batch": f"B{i % 4}",
                "concentration": round(concentration * (1000 if unit == "ug/L" else 1), 4),
                "concentration_unit": unit,
                "water_temperature_c": "" if i % 4 == 2 else temperature,
                "review_required": review,
                "post_review_flag": review,
                "workflow_status": "reviewed" if review else "cleared",
            }
        )
    samples.append(samples[19].copy())
    manifest = []
    for name, rows in {
        "cycles.csv": cycles,
        "machines.csv": machines,
        "samples.csv": samples,
        "sites.csv": sites,
    }.items():
        path = destination / name
        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        manifest.append(
            {
                "path": name,
                "rows": len(rows),
                "size_bytes": path.stat().st_size,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
        )
    (destination / "MANIFEST.yml").write_text(
        yaml.safe_dump(
            {
                "schema_version": 1,
                "source_id": "csmi-rehearsal-20260905",
                "licence": "CC-BY-4.0",
                "generated_by": "tools/build_rehearsal_data.py",
                "files": manifest,
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    build()
