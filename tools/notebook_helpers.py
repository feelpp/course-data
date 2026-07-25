"""Shared helpers for the JAX notebook-native exception."""

from __future__ import annotations

import hashlib
from typing import Any

import nbformat


def markdown(source: str, tags: list[str] | None = None) -> Any:
    return nbformat.v4.new_markdown_cell(source, metadata={"tags": tags or []})


def code(
    source: str,
    tags: list[str] | None = None,
    student_source: str | None = None,
) -> Any:
    metadata: dict[str, Any] = {"tags": tags or []}
    if student_source is not None:
        metadata["course"] = {"student_source": student_source}
    return nbformat.v4.new_code_cell(source, metadata=metadata)


def notebook(metadata: dict[str, Any], cells: list[Any]) -> Any:
    metadata = {
        **metadata,
        "accessibility": {
            "colour_alone_forbidden": True,
            "keyboard_only": True,
            "required_figure_contract": (
                "title, labelled axes with units, caption, text description"
            ),
        },
    }
    return nbformat.v4.new_notebook(
        cells=cells,
        metadata={
            "course": metadata,
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.12"},
        },
    )


def deterministic_cell_id(filename: str, index: int) -> str:
    return hashlib.sha256(f"{filename}:{index}".encode()).hexdigest()[:8]


LOCATOR = """from pathlib import Path

def locate(relative: str, local_name: str | None = None) -> Path:
    candidates = []
    if local_name:
        candidates.append(Path.cwd() / local_name)
    candidates.extend(root / relative for root in [Path.cwd(), *Path.cwd().parents])
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        f"Cannot find {relative}. Run from the course clone or place the "
        "downloaded data beside this notebook."
    )
"""
