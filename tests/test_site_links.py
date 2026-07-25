from pathlib import Path

import nbformat

from tools.check_site import (
    validate_jupyter_target,
    validate_worked_example_html,
    validate_worked_example_notebook,
)


def test_jupyter_link_accepts_an_existing_local_notebook(tmp_path: Path) -> None:
    page = tmp_path / "course-data" / "foundations" / "lesson.html"
    notebook = tmp_path / "course-data" / "_attachments" / "foundations" / "lesson.ipynb"
    page.parent.mkdir(parents=True)
    notebook.parent.mkdir(parents=True)
    page.write_text("lesson", encoding="utf-8")
    notebook.write_text("{}", encoding="utf-8")

    assert (
        validate_jupyter_target(
            page, "/course-data/_attachments/foundations/lesson.ipynb", tmp_path
        )
        == []
    )


def test_jupyter_link_rejects_unresolved_external_unsafe_and_wrong_targets(tmp_path: Path) -> None:
    page = tmp_path / "course-data" / "lesson.html"
    page.parent.mkdir(parents=True)
    page.write_text("lesson", encoding="utf-8")

    assert validate_jupyter_target(page, "#", tmp_path)
    assert validate_jupyter_target(page, "https://example.org/lesson.ipynb", tmp_path)
    assert validate_jupyter_target(page, "../../outside.ipynb", tmp_path)
    assert validate_jupyter_target(page, "/course-data/_attachments/lesson.txt", tmp_path)
    assert validate_jupyter_target(page, "/course-data/_attachments/missing.ipynb", tmp_path)


def test_worked_example_notebook_requires_ordered_learning_contract() -> None:
    notebook = nbformat.v4.new_notebook(
        cells=[
            nbformat.v4.new_markdown_cell(
                "\n".join(
                    [
                        "## Context",
                        "Importance: Essential (P0)",
                        "## Method",
                        "Importance: Core (P1)",
                        "Mathematical insight — the error scale matters",
                        "## Implementation",
                        "Importance: Essential (P0)",
                        "## Results",
                        "Importance: Essential (P0)",
                        "## Conclusion",
                        "Importance: Essential (P0)",
                    ]
                )
            )
        ]
    )
    assert validate_worked_example_notebook(notebook, "lesson.ipynb") == []

    notebook.cells[0].source = notebook.cells[0].source.replace(
        "## Results\nImportance: Essential (P0)\n", ""
    )
    errors = validate_worked_example_notebook(notebook, "lesson.ipynb")
    assert any("Results heading" in error for error in errors)


def test_worked_example_html_requires_semantic_sections_and_insight() -> None:
    sections = "\n".join(
        (
            f'<div class="sect2 worked-example-{part.lower()}">'
            f'<h3 id="worked-fixture-{part.lower()}">{part}</h3></div>'
        )
        for part in ("Context", "Method", "Implementation", "Results", "Conclusion")
    )
    html = (
        sections
        + "<div>Mathematical insight — a stable theorem</div>"
        + "<strong>Mathematical insight.</strong>"
    )
    assert validate_worked_example_html(html, "lesson.html") == []

    errors = validate_worked_example_html(
        html.replace("worked-example-results", "missing-results"),
        "lesson.html",
    )
    assert any("worked-example-results" in error for error in errors)
