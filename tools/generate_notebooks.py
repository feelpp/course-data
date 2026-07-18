#!/usr/bin/env python3
"""Generate deterministic student and instructor notebooks from reviewed sources."""

from __future__ import annotations

import argparse
import copy
from pathlib import Path
from typing import Any

import nbformat

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "notebooks/instructor"
DEFAULT_OUTPUT = ROOT / "build/notebooks"
REQUIRED_METADATA = {
    "assessed",
    "concept_ids",
    "difficulty",
    "duration_minutes",
    "execution_profile",
    "language",
    "outcomes",
    "prerequisites",
    "priority",
}


def clear_execution(notebook: Any) -> None:
    for cell in notebook.cells:
        if cell.cell_type == "code":
            cell.execution_count = None
            cell.outputs = []


def validate_source(notebook: Any, path: Path) -> None:
    course = notebook.metadata.get("course", {})
    missing = sorted(REQUIRED_METADATA - set(course))
    if missing:
        raise ValueError(f"{path}: missing course metadata: {', '.join(missing)}")
    if course["language"] != "en":
        raise ValueError(f"{path}: student-facing notebook language must be en")
    for index, cell in enumerate(notebook.cells):
        tags = set(cell.metadata.get("tags", []))
        if "solution" in tags and not cell.metadata.get("course", {}).get("student_source"):
            raise ValueError(f"{path}: solution cell {index} has no student_source")


def generated_banner(source_path: Path, mode: str) -> Any:
    label = "student" if mode == "student" else "instructor"
    return nbformat.v4.new_markdown_cell(
        "\n".join(
            [
                f"> **Generated {label} notebook.**",
                "> Do not edit this generated file in the repository; "
                "edit the reviewed instructor source.",
                f"> Source: `{source_path.as_posix()}`",
            ]
        ),
        metadata={"tags": ["generated-notice"]},
    )


def transform(source: Any, source_path: Path, mode: str) -> Any:
    notebook = copy.deepcopy(source)
    validate_source(notebook, source_path)
    cells = []
    for cell in notebook.cells:
        tags = set(cell.metadata.get("tags", []))
        if mode == "student" and ({"instructor-only", "remove-cell"} & tags):
            continue
        if mode == "student" and "solution" in tags:
            student_source = cell.metadata["course"].pop("student_source")
            cell.source = (
                "".join(student_source) if isinstance(student_source, list) else student_source
            )
            cell.metadata["tags"] = sorted((tags - {"solution"}) | {"exercise"})
            if not cell.metadata.get("course"):
                cell.metadata.pop("course", None)
        cells.append(cell)
    notebook.cells = [generated_banner(source_path, mode), *cells]
    notebook.metadata["course"]["generated_variant"] = mode
    clear_execution(notebook)
    nbformat.validate(notebook)
    return notebook


def generate(source_dir: Path, output_dir: Path, mode: str) -> list[Path]:
    sources = sorted(source_dir.rglob("*.ipynb"))
    if not sources:
        raise ValueError(f"No instructor notebooks found below {source_dir}")
    outputs: list[Path] = []
    modes = ("student", "instructor") if mode == "both" else (mode,)
    for variant in modes:
        variant_root = output_dir / variant if mode == "both" else output_dir
        for source_path in sources:
            relative = source_path.relative_to(source_dir)
            destination = variant_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            source = nbformat.read(source_path, as_version=4)
            notebook = transform(source, relative, variant)
            nbformat.write(notebook, destination)
            outputs.append(destination)
    return outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--mode", choices=("student", "instructor", "both"), default="both")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    outputs = generate(args.source_dir, args.output_dir, args.mode)
    print(f"Generated {len(outputs)} notebook(s) in {args.output_dir}")


if __name__ == "__main__":
    main()
