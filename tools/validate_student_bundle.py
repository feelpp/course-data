#!/usr/bin/env python3
"""Validate the deterministic student bundle and its publication boundary."""

from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path, PurePosixPath

import nbformat

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BUNDLE = ROOT / "build/release/course-data-student-bundle.zip"
FORBIDDEN_PARTS = {"instructor", "solutions", "hidden-tests", "archive", "private"}
OPERATIONAL_TEMPLATES = {
    "templates/assessment-item-statistics.csv",
    "templates/course-retrospective.md",
    "templates/pilot-observation.md",
    "templates/release-approval.md",
}
REQUIRED_PATHS = {
    "README-STUDENT.md",
    "MANIFEST.json",
    "curriculum.yml",
    "pyproject.toml",
    "uv.lock",
    "notebooks/foundations/data-lifecycle.ipynb",
    "notebooks/foundations/baseline-synthesis.ipynb",
    "notebooks/analytical/linear-probabilistic.ipynb",
    "datasets/teaching/air-quality/MANIFEST.yml",
    "datasets/teaching/predictive-maintenance/MANIFEST.yml",
    "templates/result-card.md",
    "templates/block-feedback.csv",
    "docs/course/modules/ROOT/pages/assessment/rubric.adoc",
}


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def validate_bundle(bundle: Path = DEFAULT_BUNDLE) -> list[str]:
    errors: list[str] = []
    if not bundle.exists():
        return [f"Student bundle is missing: {bundle}"]
    with zipfile.ZipFile(bundle) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            errors.append("Bundle contains duplicate paths")
        for name in names:
            path = PurePosixPath(name)
            if path.is_absolute() or ".." in path.parts:
                errors.append(f"Unsafe archive path: {name}")
            if FORBIDDEN_PARTS & {part.lower() for part in path.parts}:
                errors.append(f"Private or quarantined path in bundle: {name}")
        missing = REQUIRED_PATHS - set(names)
        if missing:
            errors.append(f"Bundle is missing required paths: {sorted(missing)}")
        unexpected_operations = OPERATIONAL_TEMPLATES & set(names)
        if unexpected_operations:
            errors.append(
                f"Operational templates in student bundle: {sorted(unexpected_operations)}"
            )
        if "MANIFEST.json" not in names:
            return errors
        payload = json.loads(archive.read("MANIFEST.json"))
        records = {record["path"]: record for record in payload.get("files", [])}
        expected_names = set(names) - {"MANIFEST.json"}
        if set(records) != expected_names:
            errors.append("Manifest inventory disagrees with archive contents")
        for name, record in records.items():
            content = archive.read(name)
            if record.get("sha256") != digest(content):
                errors.append(f"Manifest checksum mismatch: {name}")
            if record.get("size_bytes") != len(content):
                errors.append(f"Manifest size mismatch: {name}")
        for name in names:
            if not name.endswith(".ipynb"):
                continue
            notebook = nbformat.reads(archive.read(name).decode(), as_version=4)
            for cell in notebook.cells:
                tags = set(cell.metadata.get("tags", []))
                if {"solution", "instructor-only", "remove-cell"} & tags:
                    errors.append(f"Private notebook tag in {name}")
                if cell.cell_type == "code" and (cell.outputs or cell.execution_count is not None):
                    errors.append(f"Notebook output or execution state in {name}")
    return errors


def main() -> None:
    bundle = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_BUNDLE
    errors = validate_bundle(bundle)
    if errors:
        print("Student-bundle validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(f"Student-bundle validation passed: {bundle}")


if __name__ == "__main__":
    main()
