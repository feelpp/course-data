#!/usr/bin/env python3
"""Execute generated instructor notebooks in isolated output copies."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import nbformat
from nbclient import NotebookClient

from tools.generate_notebooks import DEFAULT_SOURCE, generate

ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "build/notebooks/instructor"
EXECUTED = ROOT / "build/executed-notebooks"
ASCIIDOC_GENERATED = ROOT / "public/course-data/_attachments"


def execute(profile: str) -> list[Path]:
    if GENERATED.exists():
        shutil.rmtree(GENERATED)
    generate(DEFAULT_SOURCE, GENERATED, "instructor")
    outputs: list[Path] = []
    timeout = 180 if profile == "fast" else 900
    native_paths = [("native", path) for path in sorted(GENERATED.rglob("*.ipynb"))]
    asciidoc_paths = [
        ("asciidoc", path)
        for path in sorted(ASCIIDOC_GENERATED.rglob("*.ipynb"))
        if "notebooks" not in path.relative_to(ASCIIDOC_GENERATED).parts
    ]
    if not asciidoc_paths:
        raise RuntimeError("No AsciiDoc-generated notebooks found; run the site build first")
    for source_kind, path in [*native_paths, *asciidoc_paths]:
        notebook = nbformat.read(path, as_version=4)
        notebook_profile = notebook.metadata["course"].get("execution_profile", "full")
        if profile == "fast" and notebook_profile != "fast":
            continue
        client = NotebookClient(
            notebook,
            timeout=timeout,
            kernel_name="python3",
            resources={"metadata": {"path": str(path.parent)}},
        )
        client.execute(cwd=str(path.parent))
        source_root = GENERATED if source_kind == "native" else ASCIIDOC_GENERATED
        destination = EXECUTED / source_kind / path.relative_to(source_root)
        destination.parent.mkdir(parents=True, exist_ok=True)
        nbformat.write(notebook, destination)
        outputs.append(destination)
    if not outputs:
        raise RuntimeError(f"No notebooks selected for {profile} execution")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=("fast", "full"), default="fast")
    args = parser.parse_args()
    outputs = execute(args.profile)
    print(f"Executed {len(outputs)} {args.profile} notebook(s)")


if __name__ == "__main__":
    main()
