from pathlib import Path

import nbformat

from tools.generate_notebooks import generate
from tools.notebook_helpers import deterministic_cell_id

ROOT = Path(__file__).resolve().parents[1]


def test_student_notebook_removes_private_cells_and_outputs(tmp_path: Path) -> None:
    outputs = generate(ROOT / "notebooks/instructor", tmp_path, "student")
    assert len(outputs) == 1
    for output in outputs:
        notebook = nbformat.read(output, as_version=4)
        assert notebook.metadata["course"]["accessibility"] == {
            "colour_alone_forbidden": True,
            "keyboard_only": True,
            "required_figure_contract": (
                "title, labelled axes with units, caption, text description"
            ),
        }
        tags = [set(cell.metadata.get("tags", [])) for cell in notebook.cells]
        assert all("solution" not in cell_tags for cell_tags in tags)
        assert all("instructor-only" not in cell_tags for cell_tags in tags)
        assert any("exercise" in cell_tags for cell_tags in tags)
        assert all(not cell.outputs for cell in notebook.cells if cell.cell_type == "code")
        assert all(
            cell.execution_count is None for cell in notebook.cells if cell.cell_type == "code"
        )
        assert notebook.metadata["course"]["source_kind"] == "notebook-native"
        assert notebook.metadata["course"]["source_path"] == (
            "extensions/jax-transformations.ipynb"
        )
    assert all(
        "foundations" not in output.parts and "analytical" not in output.parts for output in outputs
    )


def test_instructor_notebook_retains_reference_checks(tmp_path: Path) -> None:
    outputs = generate(ROOT / "notebooks/instructor", tmp_path, "instructor")
    assert outputs
    assert any(
        "solution" in cell.metadata.get("tags", [])
        for output in outputs
        for cell in nbformat.read(output, as_version=4).cells
    )


def test_jax_notebook_native_source_has_deterministic_cell_ids() -> None:
    extensions = ROOT / "notebooks/instructor/extensions"
    for path in extensions.glob("*.ipynb"):
        notebook = nbformat.read(path, as_version=4)
        assert [cell.id for cell in notebook.cells] == [
            deterministic_cell_id(f"extensions/{path.name}", index)
            for index in range(len(notebook.cells))
        ]
        code_source = "\n".join(
            cell.source for cell in notebook.cells if cell.cell_type == "code"
        ).lower()
        assert "import optax" not in code_source
        assert "jax.tree" not in code_source
