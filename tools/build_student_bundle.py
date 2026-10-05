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
    Path("templates/project-starter"),
)

BUNDLE_README = """# CSMI Data Processing and Mining — student bundle

This bundle contains solution-free notebooks, prepared teaching data,
public course pages, templates, and the locked Python environment.

## Start

Follow the [Computing environment guide](https://feelpp.github.io/course-data/course-data/environment.html)
for the full steps, explanations, and help with common errors. A source copy
is included at `docs/course/modules/ROOT/pages/environment.adoc`.

### The names, before the commands

- **uv** is the terminal program that manages Python and installs libraries.
- A **virtual environment** (often shortened to **venv**) gives this project
  its own Python and libraries, separate from those used by other projects.
- **`uv venv`** is the command that creates it. **`.venv`** is the folder
  it creates inside this bundle; your notebooks stay in `notebooks/`.
- **`pyproject.toml`** is a text configuration file: it lists the required
  Python version and libraries. TOML is its format, not a Python command.
- **`uv.lock`** is a text file recording exact library versions, including
  the other libraries they need (their dependencies). It is not a command.
- **`.python-version`** contains `3.12`, the Python version uv should select.

For example, `"pandas==2.3.1"` in `pyproject.toml` asks for exactly that pandas
version. The lockfile records the full set of libraries to install. Keep both
supplied files together; uv uses them to prepare `.venv` for this course.

### 1. Install uv for your user account

Open Terminal (macOS/Linux) or PowerShell (Windows), and try `uv --version`.
If uv is missing, use the command for your operating system below, without
`sudo` or an administrator terminal. Python is not needed for this step.

macOS/Linux (also WSL, from its Linux terminal):

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close and reopen your terminal, then check `uv --version` again. Restart
VS Code too if it was open during installation. These are the commands from
the [official uv installer](https://docs.astral.sh/uv/getting-started/installation/).

### 2. Prepare the bundle's Python environment

Extract the ZIP into a new folder. In VS Code, use **File > Open Folder** to
open the folder directly containing `pyproject.toml` and `uv.lock`, then
**Terminal > New Terminal**. Run the following in that terminal:

```sh
uv venv --python 3.12
uv sync --locked
uv run --locked python -c "import sys; print(sys.version); print(sys.executable)"
uv run --locked python -c "import numpy, pandas; print(numpy.__version__, pandas.__version__)"
```

A virtual environment is a separate Python and set of libraries for this
project, kept in `.venv`. uv downloads Python 3.12 if needed. Skip `uv venv`
if this folder already has a working environment; `uv sync` also creates it
when missing. `pyproject.toml` lists the required libraries and `uv.lock`
records their exact versions. `--locked` keeps those supplied versions.
The initial downloads need Internet access. Your notebooks stay outside `.venv`.

Check that Python is 3.12.x and its path is inside this folder's `.venv`.
`uv run` uses that environment without a separate activation command.

### 3. Run the first notebook

In VS Code, install the **Python** and **Jupyter** extensions from Microsoft.
Open `notebooks/foundations/python-pandas.ipynb`. In its top-right kernel
selector, choose **Python Environments** (possibly under **Select Another
Kernel**), then Python 3.12 from this folder's `.venv`. The kernel is the
Python process that executes the cells; `ipykernel` is already supplied.

Restart the kernel and run all cells from top to bottom. The worked sensor
example gives a mean of about 21.3 degrees Celsius, with 3 available readings
and 1 missing reading. Keep the notebook inside this folder so later lessons
can find the bundled data. Record any errors for the instructor.

Next time, reopen this folder and select the same kernel. You do not need to
reinstall uv or recreate `.venv`. Keep Windows and WSL environments separate:
if using WSL, open the bundle in a VS Code window connected to WSL.

Git, Node.js and npm are not required for this student workflow.

Required P0/P1 work is CPU-only. After bundle preparation, assessments do not
require network access, a personal service account, or a GPU. Verify every file
against `MANIFEST.json`, which also records the source commit. The Downloads
page provides the ZIP SHA-256 beside the download. The website's current study
bundle is updated with the site; retain your copy and checksum. Approved tagged
releases are immutable and are listed separately on the GitHub Releases page.

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
        if not path.stem.endswith("-solution"):
            yield path
        return
    for candidate in sorted(path.rglob("*")):
        if (
            candidate.is_file()
            and "__pycache__" not in candidate.parts
            and not candidate.stem.endswith("-solution")
        ):
            yield candidate


def collect_files(student_notebooks: Path) -> dict[str, bytes]:
    files: dict[str, bytes] = {
        "README.md": BUNDLE_README.encode(),
        "README-STUDENT.md": BUNDLE_README.encode(),
    }
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
        if path.stem.endswith("-solution"):
            continue
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
        if Path(entry["source_path"]).stem.endswith("-solution"):
            continue
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
