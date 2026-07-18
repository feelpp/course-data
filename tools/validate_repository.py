#!/usr/bin/env python3
"""Validate curriculum, content metadata, snapshots, notebooks, privacy, and pins."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import nbformat
import yaml

ROOT = Path(__file__).resolve().parents[1]
UI_SHA256 = "d453b23caec62bfb33c05f2a661a2bf7303f996537ac206de95f176d9db9cd15"
PAGE_FIELDS = {
    "page-course-language",
    "page-course-concepts",
    "page-course-priority",
    "page-course-difficulty",
    "page-course-duration-minutes",
    "page-course-outcomes",
    "page-course-prerequisites",
    "page-course-assessed",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_header(path: Path) -> dict[str, str]:
    attributes: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines()[1:]:
        match = re.match(r":([^:]+):\s*(.*)", line)
        if match:
            attributes[match.group(1)] = match.group(2)
        elif line.strip() and not line.startswith("//"):
            break
    return attributes


def split_values(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def load_curriculum(errors: list[str]) -> tuple[dict[str, Any], set[str], set[str]]:
    curriculum = yaml.safe_load((ROOT / "curriculum.yml").read_text(encoding="utf-8"))
    weights = sum(item["weight_percent"] for item in curriculum["assessments"])
    if weights != 100:
        errors.append(f"Assessment weights total {weights}, expected 100")
    blocks = curriculum["schedule"]
    hours = len(blocks) * curriculum["course"]["block_duration_hours"]
    if hours != curriculum["course"]["contact_hours"]:
        errors.append(f"Schedule contains {hours} hours, expected contact-hour total")
    concepts = {item["id"] for item in curriculum["concepts"]}
    outcomes = {item["id"] for item in curriculum["learning_outcomes"]}
    if len(concepts) != len(curriculum["concepts"]):
        errors.append("Curriculum concept identifiers are not unique")
    return curriculum, concepts, outcomes


def validate_pages(concepts: set[str], outcomes: set[str], errors: list[str]) -> None:
    for path in sorted((ROOT / "docs/course/modules").rglob("*.adoc")):
        if path.name == "nav.adoc":
            continue
        attrs = parse_header(path)
        missing = sorted(PAGE_FIELDS - set(attrs))
        if missing:
            errors.append(f"{path.relative_to(ROOT)}: missing page metadata {missing}")
            continue
        if attrs["page-course-language"] != "en":
            errors.append(f"{path.relative_to(ROOT)}: language must be en")
        unknown_concepts = set(split_values(attrs["page-course-concepts"])) - concepts
        unknown_outcomes = set(split_values(attrs["page-course-outcomes"])) - outcomes
        if unknown_concepts:
            errors.append(f"{path.relative_to(ROOT)}: unknown concepts {sorted(unknown_concepts)}")
        if unknown_outcomes:
            errors.append(f"{path.relative_to(ROOT)}: unknown outcomes {sorted(unknown_outcomes)}")
        if attrs["page-course-priority"] not in {"P0", "P1", "P2", "P3"}:
            errors.append(f"{path.relative_to(ROOT)}: invalid priority")
        if attrs["page-course-difficulty"] not in {"D1", "D2", "D3"}:
            errors.append(f"{path.relative_to(ROOT)}: invalid difficulty")
        if attrs["page-course-assessed"] not in {"yes", "no"}:
            errors.append(f"{path.relative_to(ROOT)}: assessed must be yes or no")


def validate_notebooks(concepts: set[str], outcomes: set[str], errors: list[str]) -> None:
    for path in sorted((ROOT / "notebooks/instructor").rglob("*.ipynb")):
        notebook = nbformat.read(path, as_version=4)
        try:
            nbformat.validate(notebook)
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
            continue
        course = notebook.metadata.get("course", {})
        if course.get("language") != "en":
            errors.append(f"{path.relative_to(ROOT)}: language must be en")
        unknown_concepts = set(course.get("concept_ids", [])) - concepts
        unknown_outcomes = set(course.get("outcomes", [])) - outcomes
        if unknown_concepts:
            errors.append(f"{path.relative_to(ROOT)}: unknown concepts {sorted(unknown_concepts)}")
        if unknown_outcomes:
            errors.append(f"{path.relative_to(ROOT)}: unknown outcomes {sorted(unknown_outcomes)}")
        for index, cell in enumerate(notebook.cells):
            tags = set(cell.metadata.get("tags", []))
            if "solution" in tags and not cell.metadata.get("course", {}).get("student_source"):
                errors.append(
                    f"{path.relative_to(ROOT)}: solution cell {index} lacks student source"
                )


def validate_datasets(errors: list[str]) -> None:
    for metadata_path in sorted((ROOT / "datasets/snapshots").glob("*/SOURCE.yml")):
        metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
        snapshot = metadata_path.parent / metadata["snapshot_file"]
        if not snapshot.exists():
            errors.append(f"{snapshot.relative_to(ROOT)}: missing snapshot")
            continue
        if digest(snapshot) != metadata["snapshot_sha256"]:
            errors.append(f"{snapshot.relative_to(ROOT)}: checksum mismatch")
        if snapshot.stat().st_size != metadata["snapshot_size_bytes"]:
            errors.append(f"{snapshot.relative_to(ROOT)}: size mismatch")
        if metadata.get("licence") != "CC-BY-4.0":
            errors.append(f"{metadata_path.relative_to(ROOT)}: unexpected licence")


def validate_naming_and_privacy(errors: list[str]) -> None:
    exclusions = {"docs/analysis/20260718_starter.md"}
    ignored_roots = {"archive/raw", ".git", ".venv", "node_modules", "build", "public"}
    reserved_roadmap_token = "pha" + "se"
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT).as_posix()
        if any(relative == root or relative.startswith(f"{root}/") for root in ignored_roots):
            continue
        if reserved_roadmap_token in path.name.lower():
            errors.append(f"{relative}: roadmap sequence naming is reserved")
        if path.is_file() and relative not in exclusions:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if reserved_roadmap_token in text.lower():
                errors.append(f"{relative}: roadmap sequence terminology is reserved")
    forbidden = [ROOT / "docs/course/modules/PRIVATE", ROOT / "assessments", ROOT / "solutions"]
    for path in forbidden:
        if path.exists():
            errors.append(f"{path.relative_to(ROOT)}: private material in the public tree")
    if (ROOT / ".git").exists():
        tracked = subprocess.run(
            ["git", "ls-files", "archive/raw"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        if tracked:
            errors.append("Raw archive content is tracked by Git")


def main() -> None:
    errors: list[str] = []
    _, concepts, outcomes = load_curriculum(errors)
    validate_pages(concepts, outcomes, errors)
    validate_notebooks(concepts, outcomes, errors)
    validate_datasets(errors)
    validate_naming_and_privacy(errors)
    ui_bundle = ROOT / "vendor/antora-ui/ui-bundle-v0.53.zip"
    if not ui_bundle.exists() or digest(ui_bundle) != UI_SHA256:
        errors.append("Pinned Antora UI bundle is missing or has the wrong checksum")
    source_validation = json.loads((ROOT / "audit/source-validation.json").read_text())
    if source_validation.get("status") != "pass":
        errors.append("Source-audit validation does not pass")
    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(f"Repository validation passed: {len(concepts)} concepts, {len(outcomes)} outcomes")


if __name__ == "__main__":
    main()
