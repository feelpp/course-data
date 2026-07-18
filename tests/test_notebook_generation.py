from pathlib import Path

import nbformat

from tools.build_foundation_notebooks import deterministic_cell_id
from tools.generate_notebooks import generate

ROOT = Path(__file__).resolve().parents[1]


def test_student_notebook_removes_private_cells_and_outputs(tmp_path: Path) -> None:
    outputs = generate(ROOT / "notebooks/instructor", tmp_path, "student")
    assert len(outputs) >= 7
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
    lifecycle_path = next(path for path in outputs if path.name == "data-lifecycle.ipynb")
    lifecycle = nbformat.read(lifecycle_path, as_version=4)
    combined = "\n".join(cell.source for cell in lifecycle.cells)
    assert "Replace each None value" in combined
    assert "assert audit ==" not in combined


def test_instructor_notebook_retains_reference_checks(tmp_path: Path) -> None:
    outputs = generate(ROOT / "notebooks/instructor", tmp_path, "instructor")
    lifecycle_path = next(path for path in outputs if path.name == "data-lifecycle.ipynb")
    notebook = nbformat.read(lifecycle_path, as_version=4)
    combined = "\n".join(cell.source for cell in notebook.cells)
    assert "assert audit ==" in combined
    assert any("solution" in cell.metadata.get("tags", []) for cell in notebook.cells)


def test_built_foundation_notebooks_have_deterministic_cell_ids() -> None:
    generated_names = {
        "tabular-data.ipynb",
        "data-quality.ipynb",
        "eda-sampling.ipynb",
        "safe-pipelines.ipynb",
        "metrics-errors.ipynb",
        "baseline-synthesis.ipynb",
    }
    for name in generated_names:
        path = ROOT / "notebooks/instructor/foundations" / name
        notebook = nbformat.read(path, as_version=4)
        assert [cell.id for cell in notebook.cells] == [
            deterministic_cell_id(name, index) for index in range(len(notebook.cells))
        ]


def test_built_analytical_notebooks_have_deterministic_cell_ids() -> None:
    analytical = ROOT / "notebooks/instructor/analytical"
    for path in analytical.glob("*.ipynb"):
        notebook = nbformat.read(path, as_version=4)
        assert [cell.id for cell in notebook.cells] == [
            deterministic_cell_id(f"analytical/{path.name}", index)
            for index in range(len(notebook.cells))
        ]


def test_built_extension_notebooks_have_deterministic_cell_ids() -> None:
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
