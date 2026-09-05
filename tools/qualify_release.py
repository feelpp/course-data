#!/usr/bin/env python3
"""Compare two clean release builds and record deterministic qualification evidence."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
BUNDLE = ROOT / "build/release/course-data-student-bundle.zip"
NOTEBOOK_MANIFEST = PUBLIC / "course-data/_attachments/generated/asciidoc-notebook-manifest.json"
REPORT = ROOT / "build/release/reproducibility-report.json"
LOCKED_INPUTS = (
    ROOT / "uv.lock",
    ROOT / "package-lock.json",
    ROOT / "vendor/antora-ui/ui-bundle-v0.53.zip",
    ROOT / "vendor/npm/feelpp-antora-extensions-1.0.0-rc.7-dev.3.tgz",
    ROOT / "vendor/npm/feelpp-asciidoctor-extensions-1.0.0-rc.18-dev.2.tgz",
)


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def canonical_digest(value: Any) -> str:
    content = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return digest(content)


def tree_records(root: Path) -> list[dict[str, Any]]:
    return [
        {
            "path": path.relative_to(root).as_posix(),
            "sha256": digest(path.read_bytes()),
            "size_bytes": path.stat().st_size,
        }
        for path in sorted(root.rglob("*"))
        if path.is_file()
    ]


def git_commit() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def source_tree_records() -> list[dict[str, Any]]:
    inventory = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout.split(b"\0")
    paths = sorted(
        ROOT / relative.decode()
        for relative in inventory
        if relative and (ROOT / relative.decode()).is_file()
    )
    return [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": digest(path.read_bytes()),
            "size_bytes": path.stat().st_size,
        }
        for path in paths
    ]


def working_tree_dirty() -> bool:
    return bool(
        subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
    )


def capture_release() -> dict[str, Any]:
    required = [PUBLIC, BUNDLE, NOTEBOOK_MANIFEST, *LOCKED_INPUTS]
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Release capture is missing: {missing}")

    site = tree_records(PUBLIC)
    notebook_manifest = json.loads(NOTEBOOK_MANIFEST.read_text(encoding="utf-8"))
    with zipfile.ZipFile(BUNDLE) as archive:
        student_manifest = json.loads(archive.read("MANIFEST.json"))
        bundle_file_count = len(archive.namelist())

    locked_inputs = {
        path.relative_to(ROOT).as_posix(): digest(path.read_bytes()) for path in LOCKED_INPUTS
    }
    source = source_tree_records()
    return {
        "bundle_file_count": bundle_file_count,
        "notebook_count": len(notebook_manifest["entries"]),
        "site_file_count": len(site),
        "site_html_count": sum(record["path"].endswith(".html") for record in site),
        "site_tree_sha256": canonical_digest(site),
        "source_file_count": len(source),
        "source_tree_sha256": canonical_digest(source),
        "working_tree_dirty": working_tree_dirty(),
        "student_bundle_sha256": digest(BUNDLE.read_bytes()),
        "student_manifest_sha256": canonical_digest(student_manifest),
        "notebook_manifest_sha256": canonical_digest(notebook_manifest),
        "locked_inputs": locked_inputs,
    }


def run(command: list[str]) -> None:
    environment = {
        **os.environ,
        "PYTHONHASHSEED": "0",
        "SOURCE_DATE_EPOCH": "1767225600",
        "TZ": "UTC",
    }
    subprocess.run(command, cwd=ROOT, check=True, env=environment)


def qualify(repetitions: int = 2) -> dict[str, Any]:
    if repetitions != 2:
        raise ValueError("Release qualification requires exactly two clean builds")
    if working_tree_dirty():
        raise RuntimeError("Release qualification requires a clean committed checkout")
    run(["npm", "run", "audit"])
    captures: list[dict[str, Any]] = []
    for run_number in range(1, repetitions + 1):
        print(f"Release qualification: clean build {run_number}/{repetitions}", flush=True)
        run(["npm", "run", "clean"])
        run(["npm", "run", "release:prepare"])
        captures.append(capture_release())
        if captures[-1]["working_tree_dirty"]:
            raise RuntimeError("Release preparation changed the committed source checkout")
    if captures[0] != captures[1]:
        keys = sorted(key for key in captures[0] if captures[0][key] != captures[1][key])
        raise RuntimeError(f"Clean release builds differ in: {keys}")

    report = {
        "schema_version": 1,
        "artifact": "course-data-release-qualification",
        "commit": git_commit(),
        "repeated_clean_builds": repetitions,
        "reproducible": True,
        "human_release_status": "pending_pilot_and_named_signoff",
        "artifacts": captures[0],
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Release qualification passed: {REPORT.relative_to(ROOT)}", flush=True)
    return report


if __name__ == "__main__":
    qualify()
