"""Execute trusted Python blocks in slides.typ, then compile native Typst slides.

Run: uv run --with plotly==6.3.0 python teaching/sessions/20261020/build.py
Typst does typesetting; this local build step executes Python (not the PDF viewer).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import plotly
import plotly.graph_objects as go

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
WORK = ROOT / "build/teaching/20261020"
OUT = WORK / "output"
STAGE = WORK / "typst"
GENERATED = STAGE / "generated"
GREEN, GREY = "#155f46", "#8c9c92"


def interactive() -> None:
    """One self-contained offline file; data and outcomes match the PDF examples."""
    x = np.arange(1.0, 5.0)
    y = np.array([1.0, 3.0, 2.0, 4.0])
    scenarios = [
        (1, y, "Heures · couples A"),
        (60, y, "Minutes · couples A"),
        (1, 5 - y, "Heures · couples B"),
        (60, 5 - y, "Minutes · couples B"),
    ]
    frames = []
    for index, (scale, yy, label) in enumerate(scenarios):
        xx = scale * x
        covariance = np.cov(xx, yy, ddof=1)[0, 1]
        r = np.corrcoef(xx, yy)[0, 1]
        unit = "heures" if scale == 1 else "minutes"
        layout = go.Layout(
            title=f"{label}<br>Covariance : {covariance:.3f} {unit}·point ; Pearson : {r:.1f}",
            xaxis=dict(title=f"x ({unit})", range=[0.6 * scale, 4.4 * scale]),
            yaxis=dict(title="y (points)", range=[0.6, 4.4]),
            shapes=[
                dict(
                    type="line",
                    x0=2.5 * scale,
                    x1=2.5 * scale,
                    y0=0.6,
                    y1=4.4,
                    line=dict(color=GREY, dash="dash"),
                ),
                dict(
                    type="line",
                    x0=0.6 * scale,
                    x1=4.4 * scale,
                    y0=2.5,
                    y1=2.5,
                    line=dict(color=GREY, dash="dash"),
                ),
            ],
        )
        frames.append(
            go.Frame(
                name=str(index),
                data=[go.Scatter(x=xx, y=yy, mode="markers", marker=dict(size=18, color=GREEN))],
                layout=layout,
            )
        )
    fig = go.Figure(data=frames[0].data, layout=frames[0].layout, frames=frames)
    fig.update_layout(
        font=dict(family="Arial", size=18, color="#142a24"),
        paper_bgcolor="#faf8f2",
        plot_bgcolor="#faf8f2",
        height=640,
        margin=dict(t=115, b=110),
        sliders=[
            dict(
                active=0,
                currentvalue=dict(prefix="Expérience : "),
                steps=[
                    dict(
                        label=label,
                        method="animate",
                        args=[
                            [str(i)],
                            dict(
                                mode="immediate",
                                frame=dict(duration=0, redraw=True),
                                transition=dict(duration=0),
                            ),
                        ],
                    )
                    for i, (_, _, label) in enumerate(scenarios)
                ],
            )
        ],
    )
    html = fig.to_html(
        full_html=False,
        auto_play=False,
        include_plotlyjs=True,
        div_id="paired-variation",
        config={"displaylogo": False},
    )
    (OUT / "20261020-interactive.html").write_text(
        '<!doctype html><html lang="fr"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        "<title>Covariance et Pearson — CSMI</title>"
        "<style>.skip{position:absolute;left:1rem;top:-5rem}"
        ".skip:focus{top:1rem;background:white;padding:.6rem}"
        "body{margin:2rem;background:#faf8f2;color:#142a24;font:18px Arial;}"
        "main{max-width:1200px;margin:auto}h1{color:#155f46}</style>"
        '<a class="skip" href="#main-content">Aller au contenu principal</a>'
        '<main id="main-content">'
        "<h1>Changer les unités, puis changer les couples</h1>"
        "<p>Prédire avant de déplacer le curseur : comparer les couples A en heures puis "
        "en minutes. La relation change-t-elle ? Comparer ensuite avec les couples B.</p>"
        + html
        + "<p>Les pointillés marquent les moyennes. Une conversion positive d’unité modifie "
        "la covariance et l’écart-type par le même facteur : Pearson reste inchangé. "
        "Cela ne résout ni les liens courbes, ni les observations influentes.</p>"
        "<p>Données inventées (code Python) : <code>x=(1,2,3,4)</code>, "
        "<code>y=(1,3,2,4)</code>. Les couples B utilisent <code>5-y</code> ; "
        "ils conservent les mêmes valeurs marginales "
        "et inversent le signe du coefficient.</p>"
        "<p>Le PDF contient des figures statiques ; "
        "cette page fournit l’interaction.</p></main></html>"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publish", action="store_true", help="Update public student attachments")
    args = parser.parse_args()
    if shutil.which("typst") is None:
        raise SystemExit("Install the Typst CLI, then rerun this command (see README.md).")
    GENERATED.mkdir(parents=True, exist_ok=True)
    (OUT / "pdf").mkdir(parents=True, exist_ok=True)
    source = HERE / "slides.typ"
    lesson = ROOT / "teaching/slides/20261020-statistics.json"
    shutil.copy2(source, STAGE / "slides.typ")
    shutil.copy2(lesson, STAGE / "lesson.json")
    lesson_data = json.loads(lesson.read_text())
    assert sum(item["minutes"] for item in lesson_data["slides"]) + 20 == 240
    for name in ("paper.typ", "exercises.typ", "instructor.typ"):
        shutil.copy2(HERE / name, STAGE / name)
    subprocess.run([sys.executable, str(HERE / "build_handouts.py")], check=True)
    values = {}
    namespace = {"np": np, "plt": plt, "GREEN": GREEN, "GREY": GREY}
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 16,
            "mathtext.fontset": "cm",
            "figure.facecolor": "#faf8f2",
            "axes.facecolor": "#faf8f2",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "svg.hashsalt": "csmi-covariance-20261020",
        }
    )
    blocks = re.findall(r"#let (\w+) = ```python\n(.*?)\n```", source.read_text(), re.S)
    assert [name for name, _ in blocks] == ["pairing", "matrix", "rescaling", "limits", "influence"]
    for name, code in blocks:

        def save(fig, name=name):
            fig.tight_layout()
            fig.savefig(GENERATED / f"{name}.svg", bbox_inches="tight", metadata={"Date": None})
            plt.close(fig)

        namespace.update(save=save, record=lambda **items: values.update(items))
        exec(compile(code, f"{source.name}:{name}", "exec"), namespace)
    (GENERATED / "values.json").write_text(json.dumps(values, indent=2))
    np.testing.assert_allclose(values["S"], [[5 / 3, 4 / 3], [4 / 3, 5 / 3]])
    interactive()
    pdf = OUT / "pdf/20261020-covariance-pearson.pdf"
    subprocess.run(
        ["typst", "compile", "--root", str(STAGE), str(STAGE / "slides.typ"), str(pdf)], check=True
    )
    page_count = json.loads(
        subprocess.check_output(
            [
                "typst",
                "eval",
                "query(<slide-page-count>).map(it => it.value)",
                "--root",
                str(STAGE),
                "--in",
                str(STAGE / "slides.typ"),
            ],
            text=True,
        )
    )
    frame_ids = json.loads(
        subprocess.check_output(
            [
                "typst",
                "eval",
                "query(<frame-id>).map(it => it.value)",
                "--root",
                str(STAGE),
                "--in",
                str(STAGE / "slides.typ"),
            ],
            text=True,
        )
    )
    assert frame_ids == [item["id"] for item in lesson_data["slides"]]
    expected = len(lesson_data["slides"])
    assert page_count == [expected], (
        f"Slide overflow: expected {expected} pages; found {page_count}"
    )
    for source_name, output_name, pages in [
        ("exercises.typ", "20261020-student-exercises.pdf", 3),
        ("instructor.typ", "20261020-instructor-guide.pdf", 5),
    ]:
        subprocess.run(
            [
                "typst",
                "compile",
                "--root",
                str(STAGE),
                str(STAGE / source_name),
                str(OUT / "pdf" / output_name),
            ],
            check=True,
        )
        actual_pages = json.loads(
            subprocess.check_output(
                [
                    "typst",
                    "eval",
                    "query(<handout-page-count>).map(it => it.value)",
                    "--root",
                    str(STAGE),
                    "--in",
                    str(STAGE / source_name),
                ],
                text=True,
            )
        )
        assert actual_pages == [pages], f"Handout overflow in {source_name}: {actual_pages}"
    manifest = {
        "typst": subprocess.check_output(["typst", "--version"], text=True).strip(),
        "numpy": np.__version__,
        "matplotlib": matplotlib.__version__,
        "plotly": plotly.__version__,
        "python_blocks": [n for n, _ in blocks],
        "sources": {
            str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (
                source,
                lesson,
                Path(__file__),
                HERE / "build_handouts.py",
                HERE / "paper.typ",
                HERE / "exercises.typ",
                HERE / "instructor.typ",
                ROOT / "datasets/teaching/air-quality/observations.csv",
            )
        },
    }
    (WORK / "manifest.json").write_text(json.dumps(manifest, indent=2))
    if args.publish:
        destination = ROOT / "docs/course/modules/ROOT/attachments/slides/20261020"
        (destination / "pdf").mkdir(parents=True, exist_ok=True)
        for name in ("20261020-covariance-pearson.pdf", "20261020-student-exercises.pdf"):
            shutil.copy2(OUT / "pdf" / name, destination / "pdf" / name)
        # Store the generated third-party JS bundle as a reproducible vendor archive.
        # Antora stages it using extract_companion.py; its build needs only stdlib.
        exports = HERE / "exports"
        exports.mkdir(exist_ok=True)
        entry = ZipInfo("20261020-interactive.html", date_time=(2026, 10, 20, 0, 0, 0))
        entry.compress_type = ZIP_DEFLATED
        with ZipFile(exports / "interactive.zip", "w") as archive:
            archive.writestr(entry, (OUT / entry.filename).read_bytes())
    print(f"Compiled {pdf}; interactive companion: {OUT / '20261020-interactive.html'}")


if __name__ == "__main__":
    main()
