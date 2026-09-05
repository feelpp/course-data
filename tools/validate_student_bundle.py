#!/usr/bin/env python3
"""Validate the deterministic student bundle and its publication boundary."""

from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path, PurePosixPath

import nbformat
import yaml

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
    "notebooks/extensions/jax-transformations.ipynb",
    "notebooks/assessment/control-1-specimen.ipynb",
    "notebooks/assessment/mini-project.ipynb",
    "notebooks/assessment/control-2-specimen.ipynb",
    "notebooks/assessment/final-exam-specimen.ipynb",
    "notebooks/assessment/practice-control-1.ipynb",
    "notebooks/assessment/practice-control-2.ipynb",
    "notebooks/assessment/practice-final.ipynb",
    "datasets/teaching/rehearsal/cycles.csv",
    "datasets/teaching/rehearsal/machines.csv",
    "datasets/teaching/rehearsal/samples.csv",
    "datasets/teaching/rehearsal/sites.csv",
    "datasets/teaching/rehearsal/SOURCE.yml",
    "datasets/teaching/rehearsal/MANIFEST.yml",
    "templates/project-starter/README.md",
    "templates/project-starter/.github/workflows/check.yml",
    "templates/project-starter/uv.lock",
    "datasets/teaching/air-quality/MANIFEST.yml",
    "datasets/teaching/predictive-maintenance/MANIFEST.yml",
    "templates/result-card.md",
    "templates/block-feedback.csv",
    "docs/course/modules/ROOT/pages/assessment/rubric.adoc",
}


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def expected_notebooks(curriculum: dict) -> tuple[set[str], dict[str, str]]:
    page_root = Path("docs/course/modules/ROOT/pages")
    page_sources = [
        *curriculum["foundation_release"]["notebook_sources"],
        *curriculum["analytical_release"]["notebook_sources"],
        *curriculum["enrichment_release"]["page_notebook_sources"],
        *curriculum["practice_release"]["notebook_sources"],
        *[specimen["source"] for specimen in curriculum["exercise_release"]["public_specimens"]],
    ]
    expected = {
        (Path("notebooks") / Path(source).relative_to(page_root).with_suffix(".ipynb")).as_posix()
        for source in page_sources
    }
    native_sources: dict[str, str] = {}
    native_root = Path("notebooks/instructor")
    for exception in curriculum["enrichment_release"]["source_contract"][
        "notebook_native_exceptions"
    ]:
        relative = Path(exception["artifact"]).relative_to(native_root)
        bundle_path = (Path("notebooks") / relative).as_posix()
        expected.add(bundle_path)
        native_sources[bundle_path] = relative.as_posix()
    return expected, native_sources


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
            if {".venv", ".ruff_cache", ".pytest_cache", "__pycache__"} & set(path.parts):
                errors.append(f"Local environment or cache in bundle: {name}")
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
        curriculum = yaml.safe_load(archive.read("curriculum.yml"))
        expected_notebook_paths, native_sources = expected_notebooks(curriculum)
        actual_notebook_paths = {name for name in names if name.endswith(".ipynb")}
        if actual_notebook_paths != expected_notebook_paths:
            errors.append(
                "Notebook inventory disagrees with declared generated/public sources: "
                f"missing={sorted(expected_notebook_paths - actual_notebook_paths)}, "
                f"unexpected={sorted(actual_notebook_paths - expected_notebook_paths)}"
            )
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
            course = notebook.metadata.get("course", {})
            source_kind = course.get("source_kind")
            if source_kind not in {"asciidoc", "notebook-native"}:
                errors.append(f"Notebook has no declared source-of-truth kind: {name}")
            if source_kind == "asciidoc" and (
                course.get("artifact_variant") != "student"
                or course.get("solutions_included") is not False
            ):
                errors.append(f"AsciiDoc notebook is not solution-free student material: {name}")
            if source_kind == "notebook-native" and (
                course.get("generated_variant") != "student"
                or course.get("source_path") != native_sources.get(name)
            ):
                errors.append(
                    f"Notebook-native artifact is not the declared student variant: {name}"
                )
            exercise = course.get("exercise")
            prompt_task_ids: list[str] = []
            for cell in notebook.cells:
                tags = set(cell.metadata.get("tags", []))
                if {"solution", "instructor-only", "remove-cell"} & tags:
                    errors.append(f"Private notebook tag in {name}")
                if cell.cell_type == "code" and (cell.outputs or cell.execution_count is not None):
                    errors.append(f"Notebook output or execution state in {name}")
                if "exercise-prompt" in tags:
                    prompt_task_ids.extend(cell.metadata.get("course", {}).get("task_ids", []))
            if exercise and (
                set(prompt_task_ids) != set(exercise.get("task_ids", []))
                or len(prompt_task_ids) != len(exercise.get("task_ids", []))
            ):
                errors.append(f"Exercise prompt inventory mismatch in {name}")
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
