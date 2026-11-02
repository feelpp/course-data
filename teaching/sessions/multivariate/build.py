"""Build French Typst supports and execute the canonical English notebooks."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nbformat
import numpy as np
import pandas as pd
from nbclient import NotebookClient

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BUILD = ROOT / "build/teaching/multivariate"
OUTPUT = BUILD / "output/pdf"
ATTACHMENTS = ROOT / "docs/course/modules/ROOT/attachments/slides/multivariate"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_slides() -> dict:
    lesson = json.loads((HERE / "lesson.json").read_text())
    air = pd.read_csv(ROOT / "datasets/teaching/air-quality/observations.csv")
    plt.rcParams.update(
        {
            "font.size": 12,
            "axes.prop_cycle": matplotlib.cycler(
                color=["#155f46", "#bc6734", "#4b6b99", "#85558b"]
            ),
            "svg.hashsalt": "multivariate",
        }
    )
    stage = BUILD / "typst"
    generated = stage / "generated"
    generated.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for source in [*HERE.glob("*.typ"), HERE / "lesson.json"]:
        shutil.copy2(source, stage / source.name)
    values = {}
    for session in lesson["sessions"]:
        if session["timing_mode"] == "planned":
            assert sum(minutes for minutes, _ in session["schedule"]) == session["minutes"]
        else:
            assert session["timing_mode"] == "record" and not session["schedule"]
        source = stage / f"{session['id']}.typ"
        text = source.read_text()
        assert len(re.findall(r"#frame\[", text)) == session["slides"]
        namespace = {
            "np": np,
            "pd": pd,
            "plt": plt,
            "air": air,
            "record": lambda **items: values.update(items),
        }
        for name, code in re.findall(r"#let (\w+) = ```python\n(.*?)\n```", text, re.S):

            def save(fig, name=name):
                fig.savefig(generated / f"{name}.svg", metadata={"Date": None})
                plt.close(fig)

            namespace["save"] = save
            exec(compile(code, f"{source.name}:{name}", "exec"), namespace)
        destination = OUTPUT / f"{session['id']}.pdf"
        subprocess.run(
            ["typst", "compile", "--root", str(stage), str(source), str(destination)], check=True
        )
        expression = "query(<frame-title>).map(it => it.value)"
        titles = json.loads(
            subprocess.check_output(
                ["typst", "eval", "--root", str(stage), "--in", str(source), expression], text=True
            )
        )
        pages = json.loads(
            subprocess.check_output(
                [
                    "typst",
                    "eval",
                    "--root",
                    str(stage),
                    "--in",
                    str(source),
                    "query(<slide-page-count>).first().value",
                ],
                text=True,
            )
        )
        assert len(titles) == pages == session["slides"], (session["id"], pages, len(titles))
        print(
            f"Compiled {session['date']}: {pages} pages, {session['minutes']} minutes", flush=True
        )
    (generated / "values.json").write_text(json.dumps(values, indent=2))
    subprocess.run(
        [
            "typst",
            "compile",
            "--root",
            str(stage),
            str(stage / "instructor.typ"),
            str(OUTPUT / "instructor-guide.pdf"),
        ],
        check=True,
    )
    return values


def execute_notebooks() -> list[dict]:
    subprocess.run(["node", str(HERE / "generate_notebooks.cjs")], cwd=ROOT, check=True)
    reports = []
    for path in sorted((BUILD / "notebooks").glob("*.ipynb")):
        notebook = nbformat.read(path, as_version=4)
        assert all(not cell.get("outputs") for cell in notebook.cells)
        assert notebook.metadata.course.language == "en"
        client = NotebookClient(
            notebook,
            timeout=180,
            kernel_name="python3",
            resources={"metadata": {"path": str(ROOT)}},
        )
        client.execute(cwd=str(ROOT))
        destination = BUILD / "executed" / path.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        nbformat.write(notebook, destination)
        cells = [cell for cell in notebook.cells if cell.cell_type == "code"]
        assert all(cell.execution_count is not None for cell in cells)
        assert not any(out.output_type == "error" for cell in cells for out in cell.outputs)
        figures = sum("image/png" in out.get("data", {}) for cell in cells for out in cell.outputs)
        assert figures >= (0 if path.stem == "pca-practical" else 3)
        reports.append(
            {
                "notebook": path.name,
                "code_cells": len(cells),
                "figures": figures,
                "status": "clean-kernel pass",
            }
        )
        print(f"Executed {path.name}: {len(cells)} code cells, {figures} figures", flush=True)
    assert {report["notebook"] for report in reports} == {
        "joint-variation.ipynb",
        "matrix-geometry.ipynb",
        "pca-practical.ipynb",
    }
    return reports


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--slides-only", action="store_true")
    args = parser.parse_args()
    values = build_slides()
    reports = [] if args.slides_only else execute_notebooks()
    source_paths = [
        *HERE.glob("*.typ"),
        *HERE.glob("*.py"),
        HERE / "lesson.json",
        HERE / "generate_notebooks.cjs",
        ROOT / "docs/course/modules/ROOT/pages/sessions/joint-variation.adoc",
        ROOT / "docs/course/modules/ROOT/pages/sessions/matrix-geometry.adoc",
        ROOT / "docs/course/modules/ROOT/pages/sessions/pca-practical.adoc",
        ROOT / "datasets/teaching/air-quality/observations.csv",
        ROOT / "datasets/teaching/air-quality-seasonal/observations.csv",
    ]
    report = {
        "sources": {str(p.relative_to(ROOT)): digest(p) for p in source_paths},
        "notebooks": reports,
        "computed": values,
        "typst": subprocess.check_output(["typst", "--version"], text=True).strip(),
    }
    (BUILD / "validation.json").write_text(json.dumps(report, indent=2))
    if args.publish:
        if not reports:
            raise ValueError("Publication requires notebook execution; omit --slides-only")
        ATTACHMENTS.mkdir(parents=True, exist_ok=True)
        for name in ("session-1.pdf", "session-2.pdf"):
            shutil.copy2(OUTPUT / name, ATTACHMENTS / name)
        print("Published the two student slide decks; instructor guide remains in build/")


if __name__ == "__main__":
    main()
