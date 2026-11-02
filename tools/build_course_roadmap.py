"""Build the public SVG and offline HTML roadmap from the planned curriculum.

The dated progress note records introduced topics, not completed block numbers.
Run with --check to verify that committed generated assets are current.
"""

from __future__ import annotations

import argparse
import html
import json
import textwrap
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "docs/course/modules/ROOT"


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    source = json.loads((ROOT / "teaching/course-roadmap.json").read_text())
    curriculum = yaml.safe_load((ROOT / "curriculum.yml").read_text())
    schedule = {block["block"]: block for block in curriculum["schedule"]}
    blocks = {block["number"]: block for block in source["blocks"]}
    assert list(blocks) == list(range(1, 15)) == list(schedule)
    assert sum(sum(a["minutes"] for a in b["contact_plan"]) for b in schedule.values()) == 1680
    assert sorted(n for p in source["stages"] for n in p["blocks"]) == list(blocks)
    pages = MODULE / "pages"
    for block in blocks.values():
        assert (pages / block["page"].replace(".html", ".adoc")).exists(), block["page"]

    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1180" '
        'role="img" aria-labelledby="title desc">',
        '<title id="title">CSMI Data Processing and Mining: 14 two-hour blocks</title>',
        '<desc id="desc">Planned progression from audit and pandas to joint description, '
        "validated models and reproducible delivery. Introduced topics are shown separately; "
        "the dated delivery route is shown separately.</desc>",
        "<style>text{font-family:Arial,sans-serif;fill:#142a24}.muted{fill:#50675e}"
        ".green{fill:#155f46}.label{font-weight:bold;font-size:14px;letter-spacing:1px}</style>",
        '<rect width="1600" height="1180" fill="#faf8f2"/>',
    ]

    def text(x, y, content, size=18, css="", weight="normal"):
        svg.append(
            f'<text x="{x}" y="{y}" font-size="{size}" class="{css}" '
            f'font-weight="{weight}">{esc(content)}</text>'
        )

    def wrapped(x, y, content, width, size=18, leading=24, css=""):
        lines = textwrap.wrap(content, width=width, break_long_words=False)
        for index, line in enumerate(lines):
            text(x, y + index * leading, line, size, css)
        return y + len(lines) * leading

    text(44, 50, "FROM OBSERVATIONS TO DEFENSIBLE RESULTS", 14, "green label")
    text(44, 102, "Data Processing and Mining · CSMI M1", 38, weight="bold")
    text(
        44,
        138,
        "14 × 2 h = 28 contact hours · Planned sequence, not a record of completed classes",
        21,
    )
    svg.append('<rect x="44" y="165" width="1512" height="121" rx="12" fill="#eaf0e9"/>')
    text(64, 193, f"TEACHING POSITION · {source['asOf']}", 14, "green label")
    text(64, 227, "Introduced: " + source["introduced"], 22)
    text(64, 261, "Next: " + source["next"] + ". Introduced does not mean mastered.", 20, "green")
    for column, stage in enumerate(source["stages"]):
        x = 44 + column * 382
        text(x, 333, stage["title"], 24, "green", "bold")
        wrapped(x, 362, stage["question"], 32, 17, 22, "muted")
        for row, number in enumerate(stage["blocks"]):
            b = blocks[number]
            y = 415 + row * 169
            svg.append(
                f'<rect x="{x}" y="{y}" width="364" height="153" rx="10" '
                f'fill="white" stroke="{"#155f46" if number == 4 else "#cad6cd"}" '
                f'stroke-width="{2 if number == 4 else 1}"/>'
            )
            text(x + 15, y + 28, f"{number:02d}  {b['short']}", 20, weight="bold")
            wrapped(x + 15, y + 57, b["math"], 39, 16, 21, "green")
            wrapped(x + 15, y + 108, b["evidence"], 39, 16, 21)
    text(
        44,
        1126,
        "Every block: question → mathematical tool → code → checked claim",
        23,
        "green",
        "bold",
    )
    text(
        44,
        1160,
        "Beijing is the recurring dataset. Project work begins in Block 5. "
        "Assessments: Blocks 8 and 14.",
        18,
        "muted",
    )
    svg.append("</svg>\n")

    sections = []
    for stage in source["stages"]:
        cards = []
        for n in stage["blocks"]:
            b, plan = blocks[n], schedule[n]
            cards.append(
                f'<article id="block-{n}"><div class="tag">BLOCK {n:02d} · 2 HOURS</div>'
                f'<h3>{esc(b["short"])}</h3><p class="math">{esc(b["math"])}</p>'
                "<details><summary>Question, practice and expected evidence</summary>"
                f"<p><b>Practice:</b> {esc(b['practice'])}</p>"
                f"<p><b>Evidence:</b> {esc(b['evidence'])}</p>"
                f"<p><b>Curriculum focus:</b> {esc(plan['title'])}</p>"
                f"<p><b>Checkpoint:</b> {esc(plan['checkpoint'])}</p>"
                f'<a href="../{esc(b["page"])}">Open course reference ↗</a>'
                "</details></article>"
            )
        sections.append(
            f"<section><h2>{esc(stage['title'])}</h2>"
            f'<p>{esc(stage["question"])}</p><div class="cards">'
            + "".join(cards)
            + "</div></section>"
        )
    document = """<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CSMI course roadmap · 14 two-hour blocks</title>
<style>
*{box-sizing:border-box}
.skip{position:absolute;left:1rem;top:-5rem}
.skip:focus{top:1rem;background:white;padding:.6rem}
body{margin:0;background:#faf8f2;color:#142a24;font:18px/1.55 Arial,sans-serif}
main{max-width:1450px;margin:auto;padding:40px}h1{font-size:clamp(30px,4vw,48px);line-height:1.15}
h1,h2,h3,.math,a{color:#155f46}h2{margin-top:42px}h3{font-size:24px;margin:10px 0}
.position{background:#eaf0e9;border-left:5px solid #155f46;padding:15px 24px;margin:24px 0}
.cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}
article{background:white;padding:24px;border:1px solid #cad6cd;
border-radius:12px;scroll-margin-top:20px}
.tag{font-size:13px;font-weight:bold;letter-spacing:1px;color:#50675e}summary{cursor:pointer}
summary:hover,a:hover{color:#153cb3}details[open] summary{font-weight:bold}
a:focus-visible,summary:focus-visible{outline:3px solid #e1a945;outline-offset:4px}
@media(max-width:700px){main{padding:22px}.cards{grid-template-columns:1fr}}
@media print{details>*{display:block}summary{display:none}article{break-inside:avoid}}
</style><a class="skip" href="#main-content">Skip to main content</a>
<main id="main-content"><p>CSMI M1 · Data Processing and Mining</p>
<h1>From observations to defensible results</h1>
<p>14 × 2 h = 28 contact hours. This is the planned sequence;
actual teaching progress is recorded separately.</p>
"""
    document += (
        f'<aside class="position"><b>Teaching position · {esc(source["asOf"])}</b>'
        f"<p>Introduced: {esc(source['introduced'])}.</p><p>Next: {esc(source['next'])}.</p>"
        "<p>Introduced does not mean mastered. Blocks are not marked complete.</p></aside>"
        "<p>Open a block for the practical work, mathematical tools and expected evidence. "
        "The project starts in Block 5; Controls 1 and 2 are in Blocks 8 and 14.</p>"
        + "".join(sections)
        + "<footer><p>Across the course: formulate a question, calculate, check and explain. "
        "Beijing provides a recurring context; "
        "deep learning and full MLOps remain beyond this core.</p>"
        '<p><a href="../course-map.html">Full timetable and preparation budget ↗</a></p>'
        "</footer></main></html>\n"
    )
    outputs = {
        MODULE / "images/course-roadmap.svg": "\n".join(svg),
        MODULE / "attachments/course-roadmap.html": document,
    }
    for path, value in outputs.items():
        if args.check:
            if not path.exists() or path.read_text() != value:
                raise SystemExit(f"Stale roadmap asset: {path.relative_to(ROOT)}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(value)
    print(
        "Roadmap assets are current" if args.check else "Built course roadmap SVG and offline HTML"
    )


if __name__ == "__main__":
    main()
