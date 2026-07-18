from pathlib import Path

import nbformat

from tools.generate_notebooks import generate

ROOT = Path(__file__).resolve().parents[1]


def test_student_notebook_removes_private_cells_and_outputs(tmp_path: Path) -> None:
    outputs = generate(ROOT / "notebooks/instructor", tmp_path, "student")
    assert len(outputs) == 1
    notebook = nbformat.read(outputs[0], as_version=4)
    tags = [set(cell.metadata.get("tags", [])) for cell in notebook.cells]
    assert all("solution" not in cell_tags for cell_tags in tags)
    assert all("instructor-only" not in cell_tags for cell_tags in tags)
    assert any("exercise" in cell_tags for cell_tags in tags)
    assert all(not cell.outputs for cell in notebook.cells if cell.cell_type == "code")
    assert all(cell.execution_count is None for cell in notebook.cells if cell.cell_type == "code")
    combined = "\n".join(cell.source for cell in notebook.cells)
    assert "Replace each None value" in combined
    assert "assert audit ==" not in combined


def test_instructor_notebook_retains_reference_checks(tmp_path: Path) -> None:
    outputs = generate(ROOT / "notebooks/instructor", tmp_path, "instructor")
    notebook = nbformat.read(outputs[0], as_version=4)
    combined = "\n".join(cell.source for cell in notebook.cells)
    assert "assert audit ==" in combined
    assert any("solution" in cell.metadata.get("tags", []) for cell in notebook.cells)
