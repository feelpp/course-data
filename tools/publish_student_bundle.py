#!/usr/bin/env python3
"""Package the current student bundle with the site after Antora generates notebooks."""

from __future__ import annotations

import shutil
from pathlib import Path

from tools.build_student_bundle import build_bundle
from tools.validate_student_bundle import validate_bundle

ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS = ROOT / "public/course-data/_downloads"


def publish_bundle() -> Path:
    bundle = build_bundle()
    errors = validate_bundle(bundle)
    if errors:
        raise RuntimeError("Student bundle cannot be published:\n" + "\n".join(errors))
    DOWNLOADS.mkdir(parents=True, exist_ok=True)
    for source in (bundle, bundle.with_suffix(".zip.sha256")):
        shutil.copy2(source, DOWNLOADS / source.name)
    print(f"Published validated student bundle and checksum in {DOWNLOADS.relative_to(ROOT)}")
    return DOWNLOADS / bundle.name


if __name__ == "__main__":
    publish_bundle()
