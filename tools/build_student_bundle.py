#!/usr/bin/env python3
"""Build a deterministic, solution-free student release bundle."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import zipfile
from pathlib import Path

from tools.generate_notebooks import generate

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "build/release/course-data-student-bundle.zip"
FIXED_ZIP_TIME = (2026, 1, 1, 0, 0, 0)

SOURCE_PATHS = (
    Path(".python-version"),
    Path("LICENSE.md"),
    Path("README.md"),
    Path("curriculum.yml"),
    Path("pyproject.toml"),
    Path("uv.lock"),
    Path("LICENSES"),
    Path("datasets/teaching"),
    Path("docs/course/modules/ROOT/nav.adoc"),
    Path("docs/course/modules/ROOT/pages"),
    Path("docs/course/modules/ROOT/images"),
)

STUDENT_TEMPLATE_PATHS = (
    Path("templates/ai-notes"),
    Path("templates/block-feedback.csv"),
    Path("templates/data-contract.yml"),
    Path("templates/dataset-datasheet.md"),
    Path("templates/reproducibility-manifest.yml"),
    Path("templates/result-card.md"),
)

BUNDLE_README = """# CSMI Data Processing and Mining — student bundle

This immutable bundle contains solution-free notebooks, prepared teaching data,
public course pages, templates, and the locked Python environment.

## Start

1. Install CPython 3.12 and `uv`.
2. Run `uv sync --locked --all-groups` from this directory.
3. Open a notebook below `notebooks/` in a Jupyter-compatible editor.
4. Restart the kernel and run cells from top to bottom.

Required P0/P1 work is CPU-only. After bundle preparation, assessments do not
require network access, a personal service account, or a GPU. Verify every file
against `MANIFEST.json`; the release page publishes the ZIP SHA-256.

Optional kernel, calibration, tracking, and drift notebooks use the required
CPU environment but are outside assessed completion. The optional JAX notebook
requires `uv sync --locked --all-groups --extra extensions`; missing optional
dependencies do not block required P0/P1 notebooks.

The bundle intentionally excludes instructor solutions, hidden tests, live
assessments, private review records, and quarantined raw source material.
Public assessment specimens are generated from the same AsciiDoc as their
webpages and carry solution-free exercise metadata.
"""


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def git_commit() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def iter_files(path: Path):
    if path.is_file():
        yield path
        return
    for candidate in sorted(path.rglob("*")):
        if candidate.is_file() and "__pycache__" not in candidate.parts:
            yield candidate


def collect_files(student_notebooks: Path) -> dict[str, bytes]:
    files: dict[str, bytes] = {"README-STUDENT.md": BUNDLE_README.encode()}
    for relative in SOURCE_PATHS:
        source = ROOT / relative
        if not source.exists():
            raise FileNotFoundError(relative)
        for path in iter_files(source):
            archive_name = path.relative_to(ROOT).as_posix()
            files[archive_name] = path.read_bytes()
    for relative in STUDENT_TEMPLATE_PATHS:
        source = ROOT / relative
        if not source.exists():
            raise FileNotFoundError(relative)
        for path in iter_files(source):
            archive_name = path.relative_to(ROOT).as_posix()
            files[archive_name] = path.read_bytes()
    for path in sorted(student_notebooks.rglob("*.ipynb")):
        archive_name = (Path("notebooks") / path.relative_to(student_notebooks)).as_posix()
        files[archive_name] = path.read_bytes()
    return files


def manifest(files: dict[str, bytes]) -> bytes:
    records = [
        {"path": path, "sha256": sha256_bytes(content), "size_bytes": len(content)}
        for path, content in sorted(files.items())
    ]
    payload = {
        "schema_version": 1,
        "artifact": "course-data-student-bundle",
        "commit": git_commit(),
        "files": records,
    }
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()


def write_entry(archive: zipfile.ZipFile, name: str, content: bytes) -> None:
    info = zipfile.ZipInfo(name, FIXED_ZIP_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, content)


def build_bundle(output: Path = DEFAULT_OUTPUT) -> Path:
    student_root = ROOT / "build/notebooks/release-student"
    if student_root.exists():
        shutil.rmtree(student_root)
    generate(ROOT / "notebooks/instructor", student_root, "student")
    manifest_path = (
        ROOT / "public/course-data/_attachments/generated/asciidoc-notebook-manifest.json"
    )
    if not manifest_path.exists():
        raise FileNotFoundError("Build the Antora site before preparing the student bundle")
    generated_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for entry in generated_manifest["entries"]:
        source = ROOT / "public" / entry["notebook_url"].lstrip("/")
        relative = Path(entry["source_path"]).with_suffix(".ipynb")
        destination = student_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    files = collect_files(student_root)
    files["MANIFEST.json"] = manifest(files)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w") as archive:
        for name, content in sorted(files.items()):
            write_entry(archive, name, content)
    digest_path = output.with_suffix(output.suffix + ".sha256")
    digest_path.write_text(f"{sha256_bytes(output.read_bytes())}  {output.name}\n")
    print(f"Built {output} with {len(files)} files")
    return output


if __name__ == "__main__":
    build_bundle()
