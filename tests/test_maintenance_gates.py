import json
import os
import shlex
import subprocess
from pathlib import Path

import pytest

from tools import validate_repository

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    ("report", "status", "allowed"),
    [
        ({"vulnerabilities": {}}, 0, True),
        ({"vulnerabilities": {"a": {"severity": "moderate"}}}, 1, True),
        ({"vulnerabilities": {"a": {"name": "a", "severity": "high"}}}, 1, False),
        ({"vulnerabilities": {"a": {"name": "a", "severity": "critical"}}}, 1, False),
        ({"error": {"code": "E503"}}, 1, False),
        ({}, 0, False),
        ({"vulnerabilities": {}}, 2, False),
    ],
)
def test_audit_gate_blocks_findings_and_incomplete_responses(tmp_path, report, status, allowed):
    npm = tmp_path / "npm"
    payload = shlex.quote(json.dumps(report))
    npm.write_text(f"#!/bin/sh\nprintf '%s' {payload}\nexit {status}\n")
    npm.chmod(0o755)
    result = subprocess.run(
        ["node", str(ROOT / "tools/audit-npm.mjs")],
        env={**os.environ, "PATH": f"{tmp_path}{os.pathsep}{os.environ['PATH']}"},
        capture_output=True,
        text=True,
    )
    assert (result.returncode == 0) is allowed, result.stderr


def test_naming_ignores_local_scratch_but_checks_public_content(tmp_path, monkeypatch):
    monkeypatch.setattr(validate_repository, "ROOT", tmp_path)
    (tmp_path / "templates").symlink_to(ROOT / "templates", target_is_directory=True)
    scratch = tmp_path / ".audit-work"
    scratch.mkdir()
    reserved = "pha" + "se"
    (scratch / f"{reserved}1.md").write_text(reserved)
    errors = []
    validate_repository.validate_naming_and_privacy(errors)
    assert not errors
    (tmp_path / "public-course-note.md").write_text(reserved)
    validate_repository.validate_naming_and_privacy(errors)
    assert any("public-course-note.md" in error for error in errors)
