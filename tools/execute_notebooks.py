#!/usr/bin/env python3
"""Execute generated instructor notebooks in isolated output copies."""

from __future__ import annotations

import argparse
from pathlib import Path

import nbformat
from nbclient import NotebookClient

from tools.generate_notebooks import DEFAULT_SOURCE, generate

ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "build/notebooks/instructor"
EXECUTED = ROOT / "build/executed-notebooks"


def execute(profile: str) -> list[Path]:
    generate(DEFAULT_SOURCE, GENERATED, "instructor")
    outputs: list[Path] = []
    timeout = 180 if profile == "fast" else 900
    for path in sorted(GENERATED.rglob("*.ipynb")):
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
        client.execute()
        destination = EXECUTED / path.relative_to(GENERATED)
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
