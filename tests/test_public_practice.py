"""Protect runnable, self-contained public practice and the student scaffold."""

import re
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest
import yaml

from tools.build_rehearsal_data import build

ROOT = Path(__file__).resolve().parents[1]


def test_rehearsal_inputs_are_reproducible_and_preserve_deliberate_defects(tmp_path):
    build(tmp_path)
    shipped = ROOT / "datasets/teaching/rehearsal"
    for generated in tmp_path.iterdir():
        assert generated.read_bytes() == (shipped / generated.name).read_bytes()
    cycles = pd.read_csv(tmp_path / "cycles.csv")
    machines = pd.read_csv(tmp_path / "machines.csv")
    samples = pd.read_csv(tmp_path / "samples.csv")
    assert machines.machine_id.is_unique
    assert cycles.cycle_id.duplicated().sum() == 1
    assert samples.sample_id.duplicated().sum() == 1
    assert set(cycles.temperature_unit) == {"degC", "K"}
    assert (cycles.temperature == -999).sum() == 1
    assert samples.groupby("instrument_batch").water_temperature_c.count().min() == 0
    assert cycles.requires_inspection.nunique() == samples.review_required.nunique() == 2


@pytest.mark.parametrize("slug", ["practice-control-1", "practice-control-2", "practice-final"])
def test_practice_runs_unanswered_offline_without_exporting_an_answer(tmp_path, slug):
    page = ROOT / f"docs/course/modules/ROOT/pages/assessment/{slug}.adoc"
    source = page.read_text()
    blocks = re.findall(r"\[source,python\]\n----\n(.*?)\n----", source, re.S)
    assert len(blocks) >= 7, "A specification-only notebook is not a runnable rehearsal"
    build(tmp_path)
    result = subprocess.run(
        [sys.executable, "-c", "\n\n".join(blocks)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=60,
        check=True,
    )
    assert "Rehearsal incomplete" in result.stdout
    assert not (tmp_path / "audit.json").exists()
    assert not (tmp_path / "result.json").exists()
    manifest = yaml.safe_load((tmp_path / "MANIFEST.yml").read_text())
    for filename in re.findall(r'pd.read_csv\(course_file\("(.*?)"\)\)', source):
        assert filename in {entry["path"] for entry in manifest["files"]}


def test_project_starter_runs_its_documented_checks():
    starter = ROOT / "templates/project-starter"
    for arguments in [
        ["-m", "src.analysis"],
        ["-m", "ruff", "check", "--no-cache", "src", "tests"],
        ["-m", "pytest", "-p", "no:cacheprovider"],
    ]:
        subprocess.run([sys.executable, *arguments], cwd=starter, check=True, timeout=60)
